# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Spyder
======

The Scientific PYthon Development EnviRonment
"""

from __future__ import print_function

import os
import os.path as osp
import subprocess
import sys
import shutil

from distutils.core import setup
from distutils.command.install_data import install_data


#==============================================================================
# Check for Python 3
#==============================================================================
PY3 = sys.version_info[0] == 3


#==============================================================================
# Minimal Python version sanity check
# Taken from the notebook setup.py -- Modified BSD License
#==============================================================================
v = sys.version_info
if v[:2] < (2, 7) or (v[0] >= 3 and v[:2] < (3, 4)):
    error = "ERROR: Spyder requires Python version 2.7 or 3.4 and above."
    print(error, file=sys.stderr)
    sys.exit(1)


#==============================================================================
# Constants
#==============================================================================
NAME = 'spyder'
LIBNAME = 'spyder'
from spyder import __version__, __project_url__


#==============================================================================
# Auxiliary functions
#==============================================================================
def get_package_data(name, extlist):
    """Return data files for package *name* with extensions in *extlist*"""
    flist = []
    # Workaround to replace os.path.relpath (not available until Python 2.6):
    offset = len(name)+len(os.pathsep)
    for dirpath, _dirnames, filenames in os.walk(name):
        for fname in filenames:
            if not fname.startswith('.') and osp.splitext(fname)[1] in extlist:
                flist.append(osp.join(dirpath, fname)[offset:])
    return flist


def get_subpackages(name):
    """Return subpackages of package *name*"""
    splist = []
    for dirpath, _dirnames, _filenames in os.walk(name):
        if osp.isfile(osp.join(dirpath, '__init__.py')):
            splist.append(".".join(dirpath.split(os.sep)))
    return splist


def get_data_files():
    """Return data_files in a platform dependent manner"""
    if sys.platform.startswith('linux'):
        if PY3:
            data_files = [('share/applications', ['scripts/spyder3.desktop']),
                          ('share/icons', ['img_src/spyder3.png']),
                          ('share/metainfo', ['scripts/spyder3.appdata.xml'])]
        else:
            data_files = [('share/applications', ['scripts/spyder.desktop']),
                          ('share/icons', ['img_src/spyder.png'])]
    elif os.name == 'nt':
        data_files = [('scripts', ['img_src/spyder.ico',
                                   'img_src/spyder_reset.ico'])]
    else:
        data_files = []
    return data_files


def get_packages():
    """Return package list"""
    packages = (
        get_subpackages(LIBNAME)
        + get_subpackages('spyder_breakpoints')
        + get_subpackages('spyder_profiler')
        + get_subpackages('spyder_pylint')
        + get_subpackages('spyder_io_dcm')
        + get_subpackages('spyder_io_hdf5')
        )
    return packages


#==============================================================================
# Make Linux detect Spyder desktop file
#==============================================================================
class MyInstallData(install_data):
    def run(self):
        install_data.run(self)
        if sys.platform.startswith('linux'):
            try:
                subprocess.call(['update-desktop-database'])
            except:
                print("ERROR: unable to update desktop database",
                      file=sys.stderr)
CMDCLASS = {'install_data': MyInstallData}


#==============================================================================
# Main scripts
#==============================================================================
# NOTE: the '[...]_win_post_install.py' script is installed even on non-Windows
# platforms due to a bug in pip installation process (see Issue 1158)
SCRIPTS = ['%s_win_post_install.py' % NAME]
if PY3 and sys.platform.startswith('linux'):
    SCRIPTS.append('spyder3')
else:
    SCRIPTS.append('spyder')


#==============================================================================
# Files added to the package
#==============================================================================
EXTLIST = ['.mo', '.svg', '.png', '.css', '.html', '.js', '.chm', '.ini',
           '.txt', '.rst', '.qss', '.ttf', '.json', '.c', '.cpp', '.java',
           '.md', '.R', '.csv', '.pyx', '.ipynb', '.xml']
if os.name == 'nt':
    SCRIPTS += ['spyder.bat']
    EXTLIST += ['.ico']


#==============================================================================
# Setup arguments
#==============================================================================
setup_args = dict(name=NAME,
      version=__version__,
      description='Scientific PYthon Development EnviRonment',
      long_description=
"""Spyder is an interactive Python development environment providing
MATLAB-like features in a simple and light-weighted software.
It also provides ready-to-use pure-Python widgets to your PyQt5
application: A source code editor with syntax highlighting and
code introspection/analysis features, NumPy array editor, dictionary
editor, Python console, etc.""",
      download_url='%s/files/%s-%s.zip' % (__project_url__, NAME, __version__),
      author="The Spyder Project Contributors",
      url=__project_url__,
      license='MIT',
      keywords='PyQt5 editor shell console widgets IDE',
      platforms=['any'],
      packages=get_packages(),
      package_data={LIBNAME: get_package_data(LIBNAME, EXTLIST),
                    'spyder_breakpoints': get_package_data('spyder_breakpoints', EXTLIST),
                    'spyder_profiler': get_package_data('spyder_profiler', EXTLIST),
                    'spyder_pylint': get_package_data('spyder_pylint', EXTLIST),
                    'spyder_io_dcm': get_package_data('spyder_io_dcm', EXTLIST),
                    'spyder_io_hdf5': get_package_data('spyder_io_hdf5', EXTLIST),
                    },
      scripts=[osp.join('scripts', fname) for fname in SCRIPTS],
      data_files=get_data_files(),
      classifiers=['License :: OSI Approved :: MIT License',
                   'Operating System :: MacOS',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Development Status :: 5 - Production/Stable',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development :: Widget Sets'],
      cmdclass=CMDCLASS)


#==============================================================================
# Setuptools deps
#==============================================================================
if any(arg == 'bdist_wheel' for arg in sys.argv):
    import setuptools     # analysis:ignore

install_requires = [
    'cloudpickle',
    'rope>=0.10.5',
    'jedi>=0.11.0',
    'pyflakes',
    'pygments>=2.0',
    'qtconsole>=4.2.0',
    'nbconvert',
    'sphinx',
    'pycodestyle',
    'pylint',
    'psutil',
    'qtawesome>=0.4.1',
    'qtpy>=1.2.0',
    'pickleshare',
    'pyzmq',
    'chardet>=2.0.0',
    'numpydoc',
    'keyring',
    # Packages for pyqt5 are only available in
    # Python 3
    'pyqt5<5.10;python_version>="3"',
    'spyder-kernels>=1.0'
]

extras_require = {
    'test:python_version == "2.7"': ['mock'],
    'test': ['pytest',
             'pytest-qt',
             'pytest-mock',
             'pytest-cov',
             'pytest-xvfb',
             'pytest-timeout',
             'mock',
             'flaky',
             'pandas',
             'scipy',
             'sympy',
             'pillow',
             'matplotlib',
             'cython'],
}

if 'setuptools' in sys.modules:
    setup_args['install_requires'] = install_requires
    setup_args['extras_require'] = extras_require

    setup_args['entry_points'] = {
        'gui_scripts': [
            '{} = spyder.app.start:main'.format(
                'spyder3' if PY3 else 'spyder')
        ]
    }

    setup_args.pop('scripts', None)


#==============================================================================
# Main setup
#==============================================================================
setup(**setup_args)
