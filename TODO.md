TODO
====

This is just a rough list of things that need to be
implemented:

* ensure that there is no overlap in the layout
  physical or in screenspace (`rect1 & rect2 & rect3`)
* Map physical layout to source image
  * Scale all viewports to a reference, either a specific viewport or maybe
  a dpi-settings (dots of original image per visible inch)
  * configurable reference point, i.e. a point on the source image, that should coincide with a specific pixel on the output. Default should be (0, 0), that is the upper left corner of the input image should coincide with the upper left corner of the finished wallpaper (Note: depending on the layout this may not actually in a visible area)
* Transform wallpaper for each output
* Save wallpaper as combined image and/or as one image 
  per output
* Read layout settings from file
* Import screen layout from RandR
* GUI frontend?
* Ability to set wallpaper directly?
