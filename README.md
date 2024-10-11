# Overview
This is just a dumb python application that does three things:
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
To install the required packages after Python has been installed and added to your `PATH` for easy access, you will just need to run `pip install` with the packages listed above, like so:
```
pip install opencv-python matplotlib argparse
```