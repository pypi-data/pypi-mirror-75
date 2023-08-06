from __future__ import absolute_import, division, print_function
from typing import Dict, Any

running_main: bool = False

Engine = None

# Object that hold tests functions used


class When(object):
    pass


Locals: Dict[str, Any] = {}

# this hold meta information for any items we will add to
# any runable object
runable_items: Dict[str, Any] = {}

# this hold meta information for any items we will add to
# the Setup object
setup_items: Dict[str, Any] = {}

# set of reporters that we can use to generate reports with
reporters: Dict[str, Any] = {}

# extention for File creation
# mapping of file class names to the class
FileTypeMap: Dict[str, Any] = {}
# mapping of file extension to class
FileExtMap: Dict[str, Any] = {}
