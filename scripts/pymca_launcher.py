# coding: utf-8
#/*##########################################################################
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
#############################################################################*/
"""Command line interface to execute main() functions in PyMca5 modules.
"""
import argparse
# import pkgutil
import os
import sys
from importlib import import_module

__authors__ = ["P. Knobel"]
__license__ = "MIT"
__date__ = "22/07/2016"

# small number of shortcut commands
shortcuts = {
    '': "PyMcaMain",
    'edfviewer': "EdfFileSimpleViewer"
# TODO
}

parser = argparse.ArgumentParser(description='pymca generic launcher')
# first command line argument
parser.add_argument('command',
                    nargs='?', default="",
                    help='name of module whose main() function you want to run')
# remaining command-line arguments
parser.add_argument('mainargs', nargs='*',
                    help='arguments passed to the main() function')

args = parser.parse_args()

if args.command in shortcuts:
    modname = shortcuts[args.command]
else:
    modname = args.command

try:
    # if command is a fully qualified module name
    m = import_module(modname)
except ImportError:
    # try prepending PyMca5
    try:
        m = import_module("PyMca5.PyMca." + modname)
    except ImportError:
        m = None

if m is None:
    print("No module or command " + args.command + " found")
    sys.exit(1)

try:
    main = getattr(m, "main")
except AttributeError:
    # if module does not have a amin function, try executing the source file
    # (is this a good idea?)
    if not args.command == '':
        # remove module or command for command-line arguments
        sys.argv = sys.argv[1:]
    fname = m.__file__
    if sys.version < '3.0':
        execfile(fname)
    else:
        exec(compile(open(fname).read(), fname, 'exec'))
else:
    # This will work for modules with a main() function
    status = main(*args.mainargs)

    # if status is an int, it is considered an exit status
    # (could be 0 for success, 1 for general errors, 2 for command line syntax error…)
    # None is equivalent to 0, any other object is printed to stderr and results
    # in an exit code of 1
    sys.exit(status)


# TODO: help (main.__doc__), rst2man
