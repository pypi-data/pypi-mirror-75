# SimplEdit

## A simple image editor

SimplEdit is a simple image editor, supporting PNG and JPEG file types. It offers various tools to easily modify an image.

![Demo Screenshot](simpledit/images/demo.png)

### Functionality

- Simple, intuitive UI
- Edit: Undo, Redo, Rotate, Flip, Crop
- Effects: Bloor, Enhance, Smooth, Pixelate, Swirl
- Filters: Invert, Grayscale, Sepia, Yellow Tint, Redwood, Aqua, Olive
- Creative: Before & After, Blending, & Custom Filters

### Supported formats

PNG, JPEG

### Supported modes

RGB, RGBA

## GitLab 

The development of SimplEdit is hosted on GitLab at https://gitlab.com/torresed/simpledit/.

## Installation Information

SimplEdit is available [via PyPI as the package simpledit](https://pypi.org/project/simpledit/).

Run this command to install the latest version from PyPI:

    pip3 install simpledit

Alternatively, install directly from source using a cloned copy of this repo:

    pip3 install /path/to/cloned/simpledit

After installing the latest version, SimplEdit can be launched using the `SimplEdit` command. SimplEdit has been tested and confirmed to work on the latest stable versions of WSL2, Ubuntu 18.04, and Arch Linux.

## Development Commands

#### Setup

Run `pip3 install -r requirements.txt`

#### Update Dependencies

Run `pip3 freeze > requirements.txt`

## Technology Stack

SimplEdit uses a number of open source projects:

- [Python 3](https://www.python.org)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [Pillow](https://python-pillow.org)
- [NumPy](https://numpy.org/)
- [SciKit](https://scikit-image.org/)

## License

SimplEdit is released under the GPLv3. For a copy of the license see the `LICENSE` file.
