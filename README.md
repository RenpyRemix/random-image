# Random Image

#### All you need is the single file [prefix_random_image.rpy](https://github.com/RenpyRemix/random-image/blob/master/prefix_random_image.rpy). Just read through the comments, perhaps tweak the prefix configurations, maybe delete the sample bits at the top, drop it in your game and use as advised.

This small script creates a displayable that dissolves between randomly shuffled images at set or random intervals.  
Also included are a few functions and configurations for using displayable prefixes to easily define the images.

These together allow a simple definition like
```py
image random_bg = "rnd_dir:images/bgs"
```
to be used to create a displayable that will read all the images from a folder and sensibly dissolve between them in a random order.

This approach has some benefits over creating each through ATL with choice blocks:
* Defining several is easier, especially if using prefixes.
* The sequencing cannot (randomly) repeat the same image twice. It shows all before reshuffling.
* It handles rollback better. (No clunking back through images as you scroll back)
* It can use random durations between each image/dissolve. (admittedly you could do that in ATL)

Included in the file are four prefix configurations:
```py

    # rnd_dir = shuffled_folder by passing a folder path
    # Uses all image files found in the stated folder
image random_bg = "rnd_dir:images/backgrounds"

    # rnd_tag = shuffled_tag by passing an image tag
    # Uses all defined images that start with the stated tag
image random_eileen = "rnd_tag:eileen"

    # rnd_lst = shuffled_list by passing colon separated images
    # Uses colons to separate a list of image files or references
image random_list = "rnd_lst:bg 1:bg 4:bg 9:bg 14"

    # rnd_tag2 = rnd_tag with static=4.0 to 10.0, dissolve=2.0 non linear
    # Same as rnd_tag, just with tweaked settings
image random_eileen2 = "rnd_tag2:eileen"
```

For more info on these, see the [Ren'Py Documentation: Displayable Prefixes](https://www.renpy.org/doc/html/displayables.html#displayable-prefix).

There really isn't much to explain about the class that is not covered by the inline comments.  
It just makes it easier to have random backgrounds or sprites in labels or screens.


[![Support me on Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/bePatron?u=19978585)
