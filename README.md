# Cobalic
This script generates an image from all available images that are in
the `images` directory. Each image is cropped to a small part and then
pasted into the composite in the place they were cropped from.
Which in the end creates a complete image with parts from every image.
All source images have to be the same size.

The following image formats are supported:
JPG, PNG, GIF (non-animated), BMP, PCX, TGA (uncompressed), TIF, LBM (and PBM), PBM (and PGM, PPM), XPM

## Examples

![](http://imgur.com/FyE0UrE.png)
![](http://imgur.com/PTkXnk7.png)
![](http://imgur.com/MCtAk4V.png)

## Hotkeys

| Hotkey      | Function                                                             |
|-------------|----------------------------------------------------------------------|
| Right arrow | 1 more horizontal image slice                                        |
| Left arrow  | 1 less horizontal image slice                                        |
| Up arrow    | 1 more vertical image slice                                          |
| Down arrow  | 1 less vertical image slice                                          |
| CTRL        | Used in conjunction with arrow keys multiplying their function by 10 |
| Left click  | Changes the clicked tile to the next image                           |
| Right click | Changes the clicked tile to the previous image                       |
| R           | Randomize all image tiles                                            |
| S           | Save the current composite image                                     |
| ESC         | Exit the program                                                     |


## Install
You need to install python. The tool was made for python 3. However it will most likely work without problems in python 2 as well. After installing python, install pygame like this: `pip install pygame` and then run the tool with `python cobalic.py`
