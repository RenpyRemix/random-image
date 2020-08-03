    ## The config settings create 4 prefixes: (see end of file)

    # rnd_dir = shuffled_folder by passing a folder path
        # show expression "rnd_dir:images/backgrounds"

    # rnd_tag = shuffled_tag by passing an image tag
        # show expression "rnd_tag:eileen"

    # rnd_lst = shuffled_list by passing colon separated images
        # show expression "rnd_lst:bg 1:bg 4:bg 9:bg 14"

    # rnd_tag2 = rnd_tag with static=4.0 to 10.0, dissolve=2.0 non linear
        # show expression "rnd_tag2:eileen"


# Examples
#
# Note that both of these, screen and label code, use displayables 
# defined prior to their use. This allows the images to play nicer
# with rollback features.
# Using them without defining them at init 
#     (e.g. show expression "rnd_dir:images/bgs" used inline) 
# would allow them to reset if rolled backed to that line.
 

image random_bg = "rnd_dir:images/bgs"

# e.g. (with an images/bgs folder and some images with tag "bg")
label prefix_random_image_example:
    show random_bg 
    # show expression "rnd_dir:images/bgs"
    show screen prefix_random_image_example_screen
    pause
    jump prefix_random_image_example ## To check it is ok looping back
    return

image screen_bg = "rnd_tag2:bg"

screen prefix_random_image_example_screen():

    drag:
        drag_offscreen True
        drag_handle (0,0, 640, 100)
        # Half size random tag image starting with bg
        # with static=(4.0,10.0), dissolve=2.0, warper="easeout_circ"
        add "screen_bg":
            zoom 0.5
            alpha 0.6


            ###########################################
            #                                         #
            #           To use in your game           #
            #                                         #
            #  Add to, adjust or whatever the prefix  #
            #  settings at the end of this. Use as    #
            #  per the shown examples (this and all   #
            #  above can be deleted if desired)       #
            #                                         #
            ###########################################




            #############################################
            #                                           #
            #  The Python function and config examples  #
            #                                           #
            #     adjust/tweak the config as wanted     #
            #                                           #
            #############################################


init -10 python:

    def get_displayable_size(d):
        """
        Return the size of the displayable d
        Should work for most displayables
        """
        if hasattr(d, "render"):

            return d.render(0,0,0,0).get_size()

        if not "." in d:

            d = renpy.display.image.ImageReference(d)._target()

        return renpy.easy.displayable(d).load().get_size()


    class RandomImage(renpy.display.layout.DynamicDisplayable, NoRollback):

        def __init__(self, **kwargs):
            """
            dynamic displayable to return a displayable that 
            dissolves between randomly chosen images

            @kwargs:
                images : list of all used images or displayables

                static : int/float/tuple for the static duration
                         if tuple, use random duration between (low, high)

                dissolve : int/float dissolve duration

                warper : string name of warper, e.g. "linear"
            """

            self.images = kwargs.get('images', [])

            if len(self.images) < 3:

                raise ValueError, "RandomImage needs 3 or more images. " \
                                  "Only received {}".format(self.images)

            self.static = kwargs.get('static', 10.0)
            self.dissolve = kwargs.get('dissolve', 1.0)
            self.warper = kwargs.get('warper', "linear")

            self.max_static = (
                self.static[1] if isinstance(self.static, (list, tuple)) 
                else self.static)

            # self.ref_name = "random_image_{0[0]}_{0[1]}".format(
            #     renpy.get_filename_line()).replace(' ','_').replace(
            #     '.','_').replace('/','_')

            # if not hasattr(store, self.ref_name):
            #     self.set_store_data()

            img_size = get_displayable_size(self.images[0])
            renpy.random.shuffle(self.images)

            self.data = [
                self.images[0], # Current image
                self.images[1], # Next image
                self.images[2:], # Remaining shuffled images
                img_size, # Size (of first image)
                0.0, # previous at value
                None, # duration until next swap
                ]

            kwargs.update( {
                '_predict_function' : self.predict_images } )

            super(RandomImage, self).__init__(self.get_random_image, **kwargs)


        def get_random_image(self, st, at, **kwargs):

            if at and at < self.data[4]: # rollback and reset
                self.data[4] = 0.0

            if self.data[5] is None:

                add_static = (
                    self.static if not isinstance(self.static, (list, tuple))
                    else renpy.python.rng.uniform(*self.static))

                self.data[5] = self.dissolve + add_static

            if at:

                cur_step = at - self.data[4]
                self.data[4] = at
                self.data[5] -= cur_step

                if self.data[5] <= 0.0:

                    # Swap (and reset some values)

                    if not self.data[2]:

                        reshuffle = [
                            k for k in self.images if k not in self.data[:2]]

                        renpy.random.shuffle(reshuffle)

                        self.data[2].extend(reshuffle)

                    self.data[0] = self.data[1]

                    self.data[1] = self.data[2].pop(0)

                    self.data[5] = None # so it recalculates a new duration


                elif self.data[5] <= self.dissolve:

                    dissolve_portion = max(0.0, min(1.0, 
                        ((self.dissolve - self.data[5]) / self.dissolve)))

                    warped_portion = renpy.atl.warpers[self.warper](
                        dissolve_portion)

                    return Composite(
                        self.data[3],
                        (0,0), self.data[0],
                        (0,0), Transform(
                            self.data[1], alpha=warped_portion)), 0.0

            return self.data[0], (0.1 if at else 0.0)


        def predict_images(self):

            return self.images 


    def shuffled_folder(s, **kwargs):
        return RandomImage(
            images=[
                k for k in renpy.list_files() 
                if k.startswith(s)
                and k.rpartition('.')[2] in ['png', 'jpg', 'webp']],
            **kwargs)

    def shuffled_tag(s, **kwargs):
        return RandomImage(
            images=[
                k for k in renpy.list_images() 
                if k.startswith(s)],
            **kwargs)

    def shuffled_list(s, **kwargs):
        return RandomImage(
            images=s.split(':'),
            **kwargs)


    config.displayable_prefix.update(
        rnd_dir = shuffled_folder,
        rnd_tag = shuffled_tag,
        rnd_lst = shuffled_list,
        rnd_tag2 = renpy.curry(shuffled_tag)(
            static=(4.0,10.0), 
            dissolve=2.0, 
            warper="easeout_circ"))

    ## These config settings create 4 prefixes: (adjust/tweak as wanted)

    # rnd_dir = shuffled_folder by passing a folder path
        # show expression "rnd_dir:images/backgrounds"

    # rnd_tag = shuffled_tag by passing an image tag
        # show expression "rnd_tag:eileen"

    # rnd_lst = shuffled_list by passing colon separated images
        # show expression "rnd_lst:bg 1:bg 4:bg 9:bg 14"

    # rnd_tag2 = rnd_tag with static=4.0 to 10.0, dissolve=2.0 non linear
        # show expression "rnd_tag2:eileen"