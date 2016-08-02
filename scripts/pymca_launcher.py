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
import sys
from importlib import import_module

__authors__ = ["P. Knobel"]
__license__ = "MIT"
__date__ = "01/08/2016"

# small number of shortcut commands
shortcuts = {
    'edfviewer': "EdfFileSimpleViewer"
    # TODO
}

parser = argparse.ArgumentParser(description=__doc__)
# first command line argument
parser.add_argument('command',
                    nargs='?', default="PyMcaMain",
                    help='Name of module whose main() function you want to' +
                         ' run, or "help" to print a help message. If this' +
                         ' argument is omitted, run "PyMcaMain"')
# remaining command-line arguments
parser.add_argument('mainargs', nargs=argparse.REMAINDER,
                    help='Arguments passed to the main() function, or name' +
                         ' of a module if command is "help"')

args = parser.parse_args()

print_docstring = False
if args.command == "help":
    if args.mainargs:
        # pymca_launcher.py help command
        print_docstring = True
        args.command = args.mainargs[0]
    else:
        # pymca_launcher.py help
        parser.print_help()
        parser.exit()

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
    print("No module " + modname + " found")
    sys.exit(1)

# help
if print_docstring:
    print("i can haz ")
    if m.__doc__ is not None:
        msg = "Module docstring:\n" + m.__doc__ + "\n\n"
    else:
        msg = "No module level docstring found\n\n"
    if hasattr(m, "main"):
        if m.main.__doc__ is not None:
            msg += "main() docstring:\n" + m.main.__doc__ + "\n"
        else:
            msg += "No docstring found for main() function\n"
    else:
        msg += "No main() function found\n"
    print(msg)
    sys.exit(0)

# remove launcher script from the command line
sys.argv = sys.argv[1:]

# run main() function
if hasattr(m, "main"):
    main = getattr(m, "main")
    status = main(*args.mainargs)
    sys.exit(status)

# try executing the source file
else:
    fname = m.__file__
    if sys.version < '3.0':
        execfile(fname)
    else:
        exec(compile(open(fname).read(), fname, 'exec'))


# TODO: rst2man
