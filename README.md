# Overview
This is just a dumb python script that does three things:
1. Detects faces in an image.
2. Swirls detected faces with a random angle and direction.
3. Dumps the result in a file named swirled_filename.fileformat where filename is the source image file's name and fileformat is the source image's file format.

# Requirements
To run this, you'll need Python 3 installed and executable from within your powershell. You can download and install Python 3 [here](https://www.python.org/downloads/) for Windows with links to other operating systems.

You will also need to install the required packages which will be covered in the Installation section:
- opencv-python
- numpy
- argparse

# Installation
To install the required packages after Python has been installed and added to your `PATH` for easy access, you will just need to run `pip install` in a terminal with the packages listed above, like so:
```
pip install opencv-python numpy matplotlib argparse
```

# Help
You may look at a description of the arguments at any time by invoking the `--help` argument, like so:
```
python3 swirl-faces.py --help
```

# Example Usage
This application is invoked from the command line via `python. Here is an example usage of targeting one file with an explanation on the params being used. Image was kindly provided by a friend.
### Input:

### CLI:
```
python3.exe swirl-faces.py --anime -t 1 -min 180 -max 720 -r 1.25 -f "ffxiv_dx11_2019-05-17_21-10-14.png"
```

### Output:

### Details
Working backwards from the flags provided in the CLI example, we can see the following:
- In this example, we are targeting a single file with the `-f` option. Without this option, `swirl-faces.py` will iterate through all images in a directory and apply the swirl effect to faces detected in each image.
- Using the `-r` argument, we reduce the radius of the swirl from 2 times the size of the detected face to 1.25 times the size of the detected face.
- Using the `-max` argument, the maximum angle that can be applied to a face is set to 720 degrees, up from the default of 420.
- Using the `-min` argument, the minimum angle that can be applied to a face is set to 180, degrees, up from the default of 150.
- Using the `-t` argument, we define the rate at which the swirl increases as it reaches the center of the face. The higher the value, the more logarithmic the swirl ramps up as it reaches its center. The default here is `0.75`, but we specify `1` for a smootehr swirl.
- Lastly, we use the `-a` or `--anime` flag here to tell the script to use anime-style face detection which works better on images from FFXIV.