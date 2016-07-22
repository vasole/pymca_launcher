#
# This Python module has been developed by V.A. Sole, from the European
# Synchrotron Radiation Facility (ESRF) to make PyMca available via PyPI.
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

__authors__ = ["V.A. Sole"]
__license__ = "MIT"
__date__ = "2/07/2016"

from setuptools import setup

version = "5.1.2"
name = "pymca"
author = "ESRF - Data Analysis Unit"
description = "pymca"
f = open("README.rst")
long_description = f.read()
f.close()
classifiers = ["Development Status :: 5 - Production/Stable",
               "Environment :: Console",
               "Environment :: MacOS X",
               "Environment :: Win32 (MS Windows)",
               "Intended Audience :: Education",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: MIT License",
               "Natural Language :: English",
               "Operating System :: Unix",
               "Operating System :: MacOS",
               "Operating System :: Microsoft :: Windows",
               "Operating System :: POSIX",
               "Programming Language :: Python :: 2.7",
               "Programming Language :: Python :: 3.5",
               "Topic :: Scientific/Engineering :: Chemistry",
               "Topic :: Scientific/Engineering :: Physics",
               "Topic :: Software Development :: Libraries :: Python Modules",
               ]
install_requires = ["PyMca5>=5.1.2"]

if __name__ == "__main__":
    setup(name=name,
          version=version,
          author=author,
          classifiers=classifiers,
          description=description,
          long_description=long_description,
          install_requires=install_requires,
          )
