# Random Image

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




