# coding: utf-8
# /*#########################################################################
# Copyright (C) 2019 European Synchrotron Radiation Facility
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
__authors__ = ["V.A. Sole"]
import sys
import time
import os
import glob
import shutil
from cx_Freeze import setup, Executable, hooks
from cx_Freeze import version as cxVersion

if not sys.platform.startswith("win"):
    raise RuntimeError("Only windows supported!")
if not (sys.version.startswith("3.7") or sys.version.startswith("3.6")):
    raise RuntimeError("Only Python 3.6 and 3.7 supported!")
if cxVersion.startswith('4.'):
    raise RuntimeError("At this point only cx_Freeze 5.1.1 supported")
elif cxVersion != '5.1.1':
    print("Warning: Only cx_Freeze version 5.1.1 tested and only under windows")

if "build_exe" not in sys.argv:
    print("Usage:")
    print("python setup_cx.py build_exe")
    sys.exit()

# special modules are included completely, with their data files by scripts
# run after the actual cx_Freeze operation. You may try to add them as packages
# adding the module name as string in packages. If you add a module as special
# module, you should consider to add that module to the excludes list
packages = []
special_modules = []
excludes = []

#some standard encodings
includes = []
includes.append('encodings.ascii')
includes.append('encodings.utf_8')
includes.append('encodings.latin_1')

# exec_dict is a dictionnary whose keys are the name of the .exe files to be
# generated and the values are the paths to the scripts to be frozen.
exec_dict = {}

# Program and version are used for the eventual NSIS installer
program = ""
version = ""


# a hook to bypass cx_Freeze hooks if needed
def dummy_hook(*var, **kw):
    return

# what follows is the customization for PyMca
USE_QT = True
if USE_QT:
    # If Qt is used, there is no reason to pack tkinter
    hooks.load_tkinter = dummy_hook
    excludes.append("tcl")
    excludes.append("tk")

# Mandatory modules to be integrally included in the frozen version.
# One can add other modules here if not properly detected by cx_Freeze
# (PyQt5 and matplotlib seem to be properly handled, if not, add them
# to special_modules)
import PyMca5
import fisx
import h5py
import numpy
import matplotlib
import ctypes
import hdf5plugin

packages = ["PyMca5"] # is this line needed having PyMca5 as special module?
program = "PyMca"
version = PyMca5.version()
special_modules = [os.path.dirname(PyMca5.__file__),
                   os.path.dirname(fisx.__file__),
                   os.path.dirname(h5py.__file__),
                   os.path.dirname(numpy.__file__),
                   os.path.dirname(matplotlib.__file__),
                   os.path.dirname(ctypes.__file__),
                   os.path.dirname(hdf5plugin.__file__)]
excludes += ["numpy"]

try:
    import OpenGL
    special_modules += [os.path.dirname(OpenGL.__file__)]
except ImportError:
    print("OpenGL not available, not added to the frozen executables")

# This adds the interactive console but probably I should aim at an older
# version to reduce binary size. Tested with IPython 7.4.0
try:
    import IPython
    import pygments
    import qtconsole
    import asyncio
    import ipykernel
    import zmq
    includes.append("colorsys")
    special_modules += [os.path.dirname(IPython.__file__)]
    special_modules += [os.path.dirname(pygments.__file__)]
    special_modules += [os.path.dirname(qtconsole.__file__)]
    special_modules += [os.path.dirname(asyncio.__file__)]
    special_modules += [os.path.dirname(ipykernel.__file__)]
    special_modules += [os.path.dirname(zmq.__file__)]
except ImportError:
    print("qtconsole not available, not added to the frozen executables")

try:
    import silx
    import fabio
    special_modules += [os.path.dirname(silx.__file__),
                        os.path.dirname(fabio.__file__)]
except ImportError:
    print("silx not available, not added to the frozen executables")

try:
    import freeart
    import tomogui
    special_modules += [os.path.dirname(freeart.__file__),
                        os.path.dirname(tomogui.__file__)]
except ImportError:
    print("tomogui not available, not added to the frozen executables")

# package used by silx and probably others that is not always added properly
# always add it because it is small
try:
    import pkg_resources
    special_modules += [os.path.dirname(pkg_resources.__file__)]
    excludes += ["pkg_resources"]
except ImportError:
    print("pkg_resources could not be imported")

# other generic packages not always properly detected but that are small and
# desirable to have
import collections
special_modules += [os.path.dirname(collections.__file__)]

# no scipy (huge package not used by PyMca)
excludes += ["scipy"]

# give some time to read the output
time.sleep(2)

# executable scripts to be generated for PyMca
PyMcaDir = os.path.dirname(PyMca5.__file__)
exec_dict = {"PyMcaMain": os.path.join(PyMcaDir, "PyMcaGui", \
                                      "pymca", "PyMcaMain.py"),
            "PyMcaBatch": os.path.join(PyMcaDir, "PyMcaGui", \
                                       "pymca", "PyMcaBatch.py"),
            "QStackWidget":os.path.join(PyMcaDir, "PyMcaGui", \
                                        "pymca", "QStackWidget.py"),
            "PeakIdentifier":os.path.join(PyMcaDir, "PyMcaGui", \
                                         "physics", "xrf", "PeakIdentifier.py"),
            "EdfFileSimpleViewer": os.path.join(PyMcaDir, "PyMcaGui", \
                                                 "pymca", "EdfFileSimpleViewer.py"),
            "PyMcaPostBatch": os.path.join(PyMcaDir, "PyMcaGui", \
                                           "pymca", "PyMcaPostBatch.py"),
            "Mca2Edf": os.path.join(PyMcaDir, "PyMcaGui", \
                                    "pymca", "Mca2Edf.py"),
            "ElementsInfo":os.path.join(PyMcaDir, "PyMcaGui", \
                                        "physics", "xrf", "ElementsInfo.py"),
            }


include_files = []
for f in special_modules:
    include_files.append((f, os.path.basename(f)))

build_options = {
    "packages": packages,
    "includes": includes,
    "include_files": include_files,
    "excludes": excludes, }
    #"compressed": True, }

install_options = {}

# attempt to cleanup build directory
if os.path.exists("build"):
    try:
        shutil.rmtree("build")
    except:
        print("WARNING: Cannot cleanup build directory")
    time.sleep(0.1)

# generate intermediate scripts to deal with the path during execution
tmpDir = os.path.join("build", "tmp")
if os.path.exists(tmpDir):
    shutil.rmtree(tmpDir)
if not os.path.exists("build"):
    os.mkdir("build")
print("Creating temporary directory <%s>" % tmpDir)
os.mkdir(tmpDir)

for f in list(exec_dict.keys()):
    infile = open(exec_dict[f], "r")
    outname = os.path.join(tmpDir, os.path.basename(exec_dict[f]))
    outfile = open(outname, "w")
    outfile.write("import os\n")
    outfile.write("import ctypes\n")
    # weird, somehow writing something solves startup crashes that
    # do not occur when running in debug mode
    outfile.write("print('')\n")
    magic = 'os.environ["PATH"] += os.path.dirname(os.path.dirname(ctypes.__file__))\n'
    outfile.write(magic)
    for line in infile:
        outfile.write(line)
    outfile.close()
    infile.close()
    exec_dict[f] = outname

executables = []
for key in exec_dict:
    icon = None
    # this allows to map a different icon to each executable
    if sys.platform.startswith('win'):
        if key in ["PyMcaMain", "QStackWidget"]:
            icon = os.path.join(os.path.dirname(__file__), "icons", "PyMca.ico")
    executables.append(Executable(exec_dict[key],
                                  base="Console" if sys.platform == 'win32' else None,
                                  icon=icon))
# the actual call to cx_Freeze
setup(name='pymca',
      version=PyMca5.version(),
      description="PyMca %s" % PyMca5.version(),
      options=dict(build_exe=build_options,
                   install_exe=install_options),
      executables=executables)

# cleanup
if sys.version.startswith("3.7"):
    filesToRemove = ["MSVCP140.dll", "python37.dll"]
elif sys.version.startswith("3.6"):
    filesToRemove = ["MSVCP140.dll", "python36.dll"]
else:
    filesToRemove = []
    print("Your list of files to remove needs to be updated")

exe_win_dir = os.path.join("build",
                           "exe.win-amd64-%d.%d" %
                           (sys.version_info[0], sys.version_info[1]))

REPLACE_BIG_FILES = True
if REPLACE_BIG_FILES:
    # replace excessively big files
    # somehow some modules are bigger in the installation than just
    # copying them manually.
    destinationDir = exe_win_dir
    safe_replacement = [os.path.dirname(mod.__file__) \
                        for mod in [PyMca5, fisx, h5py, numpy, hdf5plugin] \
                        if mod is not None]
    for dirname in safe_replacement:
        destination = os.path.join(destinationDir, os.path.basename(dirname))
        if os.path.exists(destination):
            print("Deleting %s" % destination)
            shutil.rmtree(destination)
            print("Deleted")
    for dirname in safe_replacement:
        destination = os.path.join(destinationDir, os.path.basename(dirname))
        print("Copying %s" % destination)
        shutil.copytree(dirname, destination)


REMOVE_DUPLICATED_MODULES = True
if REMOVE_DUPLICATED_MODULES:
    # remove duplicated modules
    import shutil
    destinationDir = os.path.join(exe_win_dir, "lib")
    for dirname in special_modules:
        destination = os.path.join(destinationDir, os.path.basename(dirname))
        if os.path.exists(destination):
            print("Deleting %s" % destination)
            shutil.rmtree(destination)
            print("Deleted")
        else:
            print("Not existing %s" % destination)
            time.sleep(0.1)

    # remove Qt binary files (qml and translation might be needed)
    for item in ["bin", "qml", "translations"]:
        destination = os.path.join(destinationDir,
                               "PyQt5","Qt",item)
        if os.path.exists(destination):
            print("Deleting %s" % destination)
            shutil.rmtree(destination)
            print("Deleted")
        else:
            print("NOT DELETING ", destination)

REMOVE_REPEATED_DLL = True
if REMOVE_REPEATED_DLL:
    work0 = []
    work1 = []
    for root, directory, files in os.walk("build"):
        for fname in files:
            if fname in filesToRemove:
                work0.append(os.path.join(root, fname))
        for dire in directory:
            if dire == "__pycache__":
                work1.append(os.path.join(root, dire))

    for item in work0[2:]:
        os.remove(item)

    work1.reverse()
    for item in work1:
        shutil.rmtree(item)

#  generation of the NSIS executable
nsis = os.path.join("\Program Files (x86)", "NSIS", "makensis.exe")
if sys.platform.startswith("win") and os.path.exists(nsis):
    # check if we can perform the packaging
    outFile = "nsisscript.nsi"
    f = open("nsisscript.nsi.in", "r")
    content = f.readlines()
    f.close()
    if os.path.exists(outFile):
        os.remove(outFile)
    pymcaexe = "%s%s-win64.exe" % (program.lower(), version)
    if os.path.exists(pymcaexe):
        os.remove(pymcaexe)
    frozenDir = os.path.join(".", exe_win_dir)
    f = open(outFile, "w")
    for line in content:
        if "__VERSION__" in line:
            line = line.replace("__VERSION__", version)
        if "__PROGRAM__" in line:
            line = line.replace("__PROGRAM__", program)
        if "__OUTFILE__" in line:
            line = line.replace("__OUTFILE__", pymcaexe)
        if "__SOURCE_DIRECTORY__" in line:
            line = line.replace("__SOURCE_DIRECTORY__", frozenDir)
        f.write(line)
    f.close()
    cmd = '"%s" %s' % (nsis, outFile)
    print(cmd)
    os.system(cmd)

