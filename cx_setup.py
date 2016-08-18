import os.path
import platform
from cx_Freeze import setup, Executable

import PyMca5

try:
    import matplotlib
except ImportError:
    matplotlib = None

special_modules = [matplotlib, PyMca5]
special_modules_dir = [os.path.dirname(mod.__file__) for mod in special_modules if mod is not None]
include_files = [(dir_, os.path.basename(dir_)) for dir_ in special_modules_dir]

excludes = []
packages = ["PyMca5"]

build_options = {
    "packages": packages,
    "include_files": include_files,
    "excludes": excludes,
    "compressed": True,}

install_options = {}

executables = [
    Executable('scripts/pymca_launcher',
               base="Win32GUI" if platform.system() == 'Windows' else None,
               # base="Console" if platform.system() == 'Windows' else None,
               compress=True)
]

setup(name='pymca',
      version=PyMca5.version(),
      description="PyMca %s" % PyMca5.version(),
      options=dict(build_exe=build_options,
                   install_exe=install_options),
      executables=executables)
