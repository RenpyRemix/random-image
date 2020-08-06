# Random Image

This small script creates a displayable that dissolves between randomly shuffled images at set or random intervals. Also included are a few functions and configurations for using displayable prefixes to easily define the images.

These together allow a simple definition like
```py
image random_bg = "rnd_dir:images/bgs"
```
to be used to create a displayable that will read all the images from a folder and sensibly dissolve between them in a random order.
