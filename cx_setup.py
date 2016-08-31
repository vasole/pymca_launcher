# coding: utf-8
# /*#########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
from cx_Freeze import setup, Executable
import os
import sys, glob

import PyMca5
import fisx
import hdf5plugin
try:
    import h5py
except ImportError:
    h5py = None
try:
    import ctypes
    import OpenGL
    from PyMca5 import Object3D
except ImportError:
    Object3D = None
    ctypes = None
    OpenGL = None

# import silx.resources
# SILX_DATA_DIR = os.path.dirname(silx.resources.__file__)

# special modules are included completely, with their data files
special_modules = [PyMca5, fisx, h5py, OpenGL, hdf5plugin, ctypes]
special_modules_dir = [os.path.dirname(mod.__file__) for mod in special_modules if mod is not None]
include_files = [(dir_, os.path.basename(dir_)) for dir_ in special_modules_dir]



# include_files.append((SILX_DATA_DIR,  os.path.join('silx', 'resources')))

packages = ["PyMca5"]  # ["silx"]

includes = []


# modules excluded from library.zip
excludes = ["collections.abc", "tcl", "tk", "OpenGL", "scipy", ]

build_options = {
    "packages": packages,
    "includes": includes,
    "include_files": include_files,
    "excludes": excludes, }
    #"compressed": True, }

install_options = {}

executables = [
    Executable('scripts/pymca_launcher',
               # base="Win32GUI" if sys.platform == 'win32' else None,
               base="Console" if sys.platform == 'win32' else None,)
               # compress=True)
]

setup(name='pymca',
      version=PyMca5.version(),
      description="PyMca %s" % PyMca5.version(),
      options=dict(build_exe=build_options,
                   install_exe=install_options),
      executables=executables)
