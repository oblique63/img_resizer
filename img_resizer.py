#! /usr/bin/python

# Program: Image Resizer
# Author: Enrique Gavidia
# E-mail: enrique@enriquegavidia.com
# License: TBD
# Date: 2008-2010

from src.resizer import Resizer
from src.interface import display_interface

imgResizer = Resizer()

# If user gives no commandline arguments, display user interface
if len(imgResizer.path_input()) < 1:
    display_interface()
else:
    imgResizer.resize()

