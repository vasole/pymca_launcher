#
# These Python module have been developed by V.A. Sole, from the European
# Synchrotron Radiation Facility (ESRF) to build a frozen version of PyMca.
# Given the nature of this work, these module can be considered public domain.
# Therefore redistribution and use in source and binary forms, with or without
# modification, are permitted provided the following disclaimer is accepted:
#
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR(S) AND THE ESRF ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR(S) AND/OR THE ESRF BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# A cx_freeze setup script to create PyMca executables
#
# Use "python cx_setup.py install"
#
# It expects a properly configured compiler.
#
# Under windows you may need to set MINGW = True (untested) if you are
# not using VS2003 (python 2.5) or VS2008 (python > 2.5)
#
# If everything works well one should find a directory in the build
# directory that contains the files needed to run the PyMca without Python
#
from cx_Freeze import setup, Executable
import cx_Freeze.hooks as _hooks
import sys
import os
import glob
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

MINGW = False
DEBUG = False

def load_PyQt4_Qt(finder, module):
    """the PyQt4.Qt module is an extension module which imports a number of
       other modules and injects their namespace into its own. It seems a
       foolish way of doing things but perhaps there is some hidden advantage
       to this technique over pure Python; ignore the absence of some of
       the modules since not every installation includes all of them."""
    mandatory_modules = ("PyQt4.QtCore", "PyQt4.QtGui", "sip")
    modules = ("PyQt4._qt", "PyQt4.QtXml", "PyQt4.QtSvg", "PyQt4.QtTest"
               "PyQt4.QtSvg", "PyQt4.Qsci", "PyQt4.QtAssistant",
               "PyQt4.QtNetwork", "PyQt4.QtOpenGL", "PyQt4.QtScript",
               "PyQt4.QtSql")

    for module_name in mandatory_modules:
        finder.IncludeModule(module_name)

    for module_name in modules:
        try:
            finder.IncludeModule(module_name)
        except ImportError:
            logger.warning("Could not import module %s", module_name)

_hooks.load_PyQt4_Qt = load_PyQt4_Qt

includes = ['encodings.ascii', 'encodings.utf_8', 'encodings.latin_1']
"""List of names of modules to include into the frozen package"""

excludes = ["Tkinter", "tkinter",
            'tcl', '_tkagg', 'Tkconstants',
            "scipy", "Numeric", "numarray",
            'qt', 'qttable', 'qtcanvas', 'Qwt5']
"""List of names of modules to exclude from the frozen package"""

include_files = []
"""List containing data files and directories to be included in the frozen
package. A file or directory is defined by a 2-tuple:
source and destination"""

special_modules = []
"""List of installation directories of modules needing to be included in
the frozen package."""


PyMcaInstallationDir = "build"
PyMcaDir = os.path.join(PyMcaInstallationDir, "PyMca5")
if sys.platform != "windows":
    PyMcaDir = PyMcaDir.replace(" ", "_")

#make sure PyMca is freshly built
if sys.platform == 'win32' and MINGW:
    # MinGW compiler needs two steps
    cmd = "python setup.py build -c mingw32 --distutils"
    if os.system(cmd):
        logger.error("Error building PyMca")
        sys.exit(1)

cmd = "python setup.py install --install-lib %s --distutils" % PyMcaInstallationDir
if os.system(cmd):
    logger.error("Error building PyMca")
    sys.exit(1)
# PyMca expected to be properly installed

# Ensure we use the PyMca we just built and we don't import from . (source repo)
sys.path = [PyMcaInstallationDir] + sys.path[1:]
try:
    import ctypes
    import OpenGL
    from PyMca5 import Object3D
except ImportError:
    logger.warning("Not including OpenGL, ctypes and logging")
else:
    includes.append("logging")
    excludes.append("OpenGL")
    special_modules.append(os.path.dirname(OpenGL.__file__))
    special_modules.append(os.path.dirname(ctypes.__file__))

import PyMca5

special_modules.append(os.path.dirname(PyMca5.__file__))

# this is critical for Qt to find image format plugins
include_files.append(("qtconffile", "qt.conf"))

# Add the qt plugins directory
import PyQt4.Qt as qt
app = qt.QApplication([])
pluginsDir = str(qt.QLibraryInfo.location(qt.QLibraryInfo.PluginsPath))
for pluginSet in glob.glob(os.path.join(pluginsDir, '*')):
    plugin = os.path.basename(pluginSet)
    if plugin in ["imageformats"]:
        if sys.platform == 'win32':
            ext = "*dll"
        else:
            if sys.platform.startswith("darwin"):
                logger.warning("WARNING: Not ready for this platform")
            #for darwin platform I use py2app
            #this only applies to linux
            ext = "*so"
        destination = os.path.join("plugins", plugin)
        fList = glob.glob(os.path.join(pluginSet, ext))
        for f in fList:
            include_files.append(
                    (f, os.path.join(destination, os.path.basename(f))))


# For the time being I leave SciPy out (it doubles the size of the package)
# try:
#     import scipy
# except ImportError:
#     scipy = None
# else:
#     special_modules.append(os.path.dirname(scipy.__file__))
scipy = None

try:
    import matplotlib
except ImportError:
    logger.warning("matplotlib could not be imported")
else:
    special_modules.append(os.path.dirname(matplotlib.__file__))


if sys.platform.lower().startswith("linux"):
    pyopencl = None
    excludes.append("pyopencl")
else:
    try:
        import pyopencl
        from PyMca5.PyMcaMath import sift
    except ImportError:
        logger.warning("pyopencl could not be imported")
        excludes.append("pyopencl")
    else:
        special_modules.append(os.path.dirname(pyopencl.__file__))
        includes.append("pytools")
        includes.append("decorator")

try:
    import mdp
except ImportError:
    pass
else:
    if mdp.__version__ > '2.5':
        special_modules.append(os.path.dirname(mdp.__file__))

try:
    import h5py
    if h5py.version.version < '1.2.0':
        includes.append('h5py._extras')
    elif h5py.version.version < '1.3.0':
        includes.extend(['h5py._stub', 'h5py._sync', 'h5py.utils'])
    elif h5py.version.version < '2.0.0':
        includes.extend(['h5py._extras', 'h5py._stub', 'h5py.utils',
                         'h5py._conv', 'h5py._proxy'])
    else:
        special_modules.append(os.path.dirname(h5py.__file__))
except ImportError:
    logger.warning("h5py could not be imported")

try:
    import fisx
    special_modules.append(os.path.dirname(fisx.__file__))
except ImportError:
    logger.error("Please install fisx module prior to freezing PyMca")
    raise

try:
    import hdf5plugin   # FIXME: dead code? or needed by cx_freeze?
except ImportError:
    logger.warning("hdf5plugin could not be imported")

if sys.platform == "win32":
    try:
        import hdf5plugin
        special_modules.append(os.path.dirname(hdf5plugin.__file__))
    except ImportError:
        logger.error("Please install hdf5plugin prior to freezing PyMca")
        raise

try:
    import IPython
    if IPython.__version__.startswith('2'):
        special_modules.append(os.path.dirname(IPython.__file__))
        includes.append("colorsys")
        import pygments
        special_modules.append(os.path.dirname(pygments.__file__))
        import zmq
        special_modules.append(os.path.dirname(zmq.__file__))
        import pygments
        #includes.append("IPython")
        #includes.append("IPython.qt")
        #includes.append("IPython.qt.console")
        #includes.append("IPython.qt.console.rich_ipython_widget")
        #includes.append("IPython.qt.inprocess")
        #includes.append("IPython.lib")
except ImportError:
    logger.warning("Console plugin not available")

if sys.version < '3.0':
    #https://bitbucket.org/anthony_tuininga/cx_freeze/issues/127/collectionssys-error
    excludes.append("collections.abc")


# special_modules is now complete, time to fill include_files
for f in special_modules:
    include_files.append((f, os.path.basename(f)))

buildOptions = dict(
        compressed=True,
        include_files=include_files,
        excludes=excludes,
        includes=includes)

install_dir = PyMcaDir + " " + PyMca5.version()
if not sys.platform.startswith('win'):
    install_dir = install_dir.replace(" ", "")
if os.path.exists(install_dir):
    try:
        def dir_cleaner(directory):
            for f in glob.glob(os.path.join(directory, '*')):
                if os.path.isfile(f):
                    try:
                        os.remove(f)
                    except:
                        print("file <%s> not deleted" % f)
                if os.path.isdir(f):
                    dir_cleaner(f)
            try:
                os.rmdir(directory)
            except OSError:
                logger.warning("directory %s not deleted", directory)

        dir_cleaner(install_dir)
    except:
        logger.error("Unexpected error while cleaning install dir:" +
                     str(sys.exc_info()))

if os.path.exists('bin'):
    for f in glob.glob(os.path.join('bin', '*')):
        os.remove(f)
    os.rmdir('bin')
installOptions = {"install_dir": install_dir}


exec_list = {"PyMcaMain": os.path.join(
                 PyMcaDir, "PyMcaGui", "pymca", "PyMcaMain.py"),
             "PyMcaBatch": os.path.join(
                 PyMcaDir, "PyMcaGui", "pymca", "PyMcaBatch.py"),
             "QStackWidget": os.path.join(
                 PyMcaDir, "PyMcaGui", "pymca", "QStackWidget.py"),
             "PeakIdentifier": os.path.join(
                 PyMcaDir, "PyMcaGui", "physics", "xrf", "PeakIdentifier.py"),
             "EdfFileSimpleViewer": os.path.join(
                 PyMcaDir, "PyMcaGui", "pymca", "EdfFileSimpleViewer.py"),
             "PyMcaPostBatch": os.path.join(
                 PyMcaDir, "PyMcaGui", "pymca", "PyMcaPostBatch.py"),
             "Mca2Edf": os.path.join(
                 PyMcaDir, "PyMcaGui", "pymca", "Mca2Edf.py"),
             "ElementsInfo": os.path.join(
                 PyMcaDir, "PyMcaGui", "physics", "xrf", "ElementsInfo.py"),
             }

for f in exec_list:
    executable = os.path.join(install_dir, f)
    if os.path.exists(executable):
        os.remove(executable)

executables = []
for key, python_module in exec_list.items():
    icon = None
    # this allows to map a different icon to each executable
    if sys.platform.startswith('win'):
        if key in ["PyMcaMain", "QStackWidget"]:
            icon = os.path.join(os.path.dirname(__file__),
                                "icons", "PyMca.ico")
    executables.append(Executable(python_module,
                                  icon=icon))

setup(
    name="PyMca5",
    version=PyMca5.version(),
    description="PyMca %s" % PyMca5.version(),
    options=dict(build_exe=buildOptions,
                 install_exe=installOptions),
    executables=executables)


if pyopencl is not None:
    # pyopencl __init__.py needs to be patched
    initFile = os.path.join(install_dir, "pyopencl", "__init__.py")
    f = open(initFile, "r")
    content = f.readlines()
    f.close()
    i = 0
    i0 = 0
    for line in content:
        if "def _find_pyopencl_include_path():" in line:
            i0 = i - 1
        elif (i0 != 0) and ("}}}" in line):
            i1 = i
            break
        i += 1
    f = open(initFile, "w")
    for line in content[:i0]:
        f.write(line)
    txt = '\n'
    txt += 'def _find_pyopencl_include_path():\n'
    txt += '     from os.path import dirname, join, realpath\n'
    txt += "     return '\"%s\"' % join(realpath(dirname(__file__)), \"cl\")"
    txt += "\n"
    txt += "\n"
    f.write(txt)
    for line in content[i1:]:
        f.write(line)
    f.close()

if not sys.platform.startswith('win'):
    #rename the executables to .exe for easier handling by the start scripts
    for f in exec_list:
        executable = os.path.join(install_dir, f)
        if os.path.exists(executable):
            os.rename(executable, executable+".exe")
        #create the start script
        text = "#!/bin/bash\n"
        text += 'if test -e "./%s.exe"; then\n' % f
        text += '    export LD_LIBRARY_PATH=./:${LD_LIBRARY_PATH}\n'
        text += '    exec ./%s.exe $*\n' % f
        text += 'else\n'
        text += '    if test -z "${PYMCAHOME}" ; then\n'
        text += '        thisdir=`dirname $0` \n'
        text += '        export PYMCAHOME=${thisdir}\n'
        text += '    fi\n'
        text += '    export LD_LIBRARY_PATH=${PYMCAHOME}:${LD_LIBRARY_PATH}\n'
        text += '    exec ${PYMCAHOME}/%s.exe $*\n' % f
        text += 'fi\n'
        nfile = open(executable,'w')
        nfile.write(text)
        nfile.close()
        os.system("chmod 775 %s" % executable)
        #generate the lowercase commands
        if f == "PyMcaMain":
            os.system("cp -f %s %s" % (executable, os.path.join(install_dir, 'pymca')))
        elif f == "QStackWidget":
            os.system("cp -f %s %s" % (executable, os.path.join(install_dir, 'pymcaroitool')))
        elif f == "EdfFileSimpleViewer":
            os.system("cp -f %s %s" % (executable, os.path.join(install_dir, 'edfviewer')))
        else:
            os.system("cp -f %s %s" % (executable,
                                       os.path.join(install_dir, f.lower())))
            if f == "PyMcaPostBatch":
                os.system("cp -f %s %s" % (executable, os.path.join(install_dir, 'rgbcorrelator')))


# cleanup
for f in glob.glob(os.path.join(os.path.dirname(__file__), "PyMca5", "*.pyc")):
    os.remove(f)

if not sys.platform.startswith('win'):
    # Unix binary ...
    for dirname in ['/lib', '/usr/lib', '/usr/X11R6/lib/']:
        for fname0 in ["libreadline.so.4",
                       "libgthread-2.0.so.0",
                       "libglib-2.0.so.0",
                       "libpng12.so.0",
                       "libfreetype.so.6",
                       "libXrender.so.1",
                       "libXxf86vm.so.1",
                       "libfontconfig.so.1",
                       "libexpat.so.0", ]:
            fname = os.path.join(dirname, fname0)
            if os.path.exists(fname):
                cmd = "cp -f %s %s" % (fname, os.path.join(install_dir, fname0))
                os.system(cmd)
        #numpy is now compiled with libgfortran at the ESRF
        for fname in glob.glob(os.path.join(dirname, "libgfortra*")):
            if os.path.exists(fname):
                cmd = "cp -f %s %s" % (fname,
                                       os.path.join(install_dir,
                                                    os.path.basename(fname)))
                os.system(cmd)

# check if the library has been created
library = os.path.join(install_dir, "library.zip")
if not os.path.exists(library):
    logger.error("Cannot find zipped library: ")
    logger.error(library)
    logger.error("Please use python cx_setup.py install")

if os.path.exists('bin'):
    for f in glob.glob(os.path.join('bin', '*')):
        os.remove(f)
    os.rmdir('bin')

if scipy is None:
    for f in ["SplinePlugins.py"]:   # FIXME: does this plugin still exist?
        plugin = os.path.join(install_dir, "PyMcaPlugins", f)
        if os.path.exists(plugin):
            logger.info("Deleting plugin %s", plugin)
            os.remove(plugin)

sys.exit(0)



