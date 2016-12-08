# -*- coding: utf-8 -*-

# A simple setup script to create an executable using matplotlib.
#
# matplotlib_eg.py is a very simple matplotlib application that demonstrates
# its use.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable
import matplotlib
import tkinter.filedialog

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {

        # Sometimes a little fine-tuning is needed
        # exclude all backends except wx
        'excludes': ['gtk', 'PyQt4', 'PyQt5','wx'],
		'includes': ['matplotlib','tkinter.filedialog'],
		#'packages': ['tkinter', 'tkfiledialog']
    }
}

executables = [
    Executable('IPTClock.py', base=base)
]

setup(name='IPTClock',
      version='0.1',
      description='IPT clock',
      executables=executables,
      options=options
      )
