##############################################################################################
#  IPTClock, a graphical countdown clock for use with the international physicist's tournament
    Copyright (C) 2016-2017  Albin Jonasson Svärdsby & Joel Magnusson

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################################

## Purpose ##
This program is written to serve the purpose of a timing and presentation tool
for the international physicist tournament. http://iptnet.info/

It is written in python 3 and is meant to be cross-platform, using tkinter as
GUI control and matplotlib for image and graphics tweaking. It should also be backwards compatible with python2.


## Dependencies ##
IPTClock has the following dependencies:

Python3 or higher

matplotlib

tkinter

Image, ImageTk from PIL  (install package python3-pil.imagetk) (it is actually pillow, a PIL fork)


(for a smaller breakdown if you want
to avoid installing the entire modules, please see the imports at the top of
IPTClock.py and Classes/iptclock_classes.py)


## (Optional) Dependencies ##
pyaudio

cx_Freeze  (for creating pre built packages: https://anthony-tuininga.github.io/cx_Freeze/)


## How to run ##
The clock is run in a terminal environment using the command:

python3 IPTClock.py

alternatively it can be run using pre build binaries found under the build folder.
For instance in the case of windows use the exe file IPTClock.exe found in
build/exe.win-ARCHITECHURE-PYTHONVER/IPTClock.exe

If you click on the count down text a popup will appear for changing the time of the present stage.

## Key bindings ##
Key bindings used by IPTClock is

-- For Linux and Window --

Ctrl+Left : Switch to previous stage

Ctrl+Right : Switch to next stage

\<F11\> : Toggle fullscreen

\<Escape\> : Exit fullscreen

Ctrl + + : Increase font size
Ctrl + = : Increase font size

Ctrl + - : Decrease font size

Ctrl + 0 : Revert to default font size

Ctrl + Enter : Start/Paus

Ctrl + r : Reset and start clock

Ctrl + j : decrease size of sponsor image

Ctrl + k : decrease size of sponsor image

Ctrl + u : Activates popup for changing the start time of the countdown. This is the same as left click on the countdown with the mouse.

Ctrl + m : Substract 5s from timer

Ctrl + n : Add 5s to timer

--For Mac--

Command+Left : Switch to previous stage

Command+Right : Switch to next stage

\<F11\> : Toggle fullscreen

\<Escape\> : Exit fullscreen

Command + + : Increase font size (Warning mind dead key, see Known bugs)

Command 0 = : Increase font size

Command + - : Decrease font size

Command + 0 : Revert to default font size

Command + Enter : Start/Paus

Command + r : Reset and start clock

Command + j : decrease size of sponsor image

Command + k : decrease size of sponsor image

Command + u : Activates popup for changing the start time of the countdown. This is the same as left click on the countdown with the mouse.

Command + m : Substract 5s from timer

Command + n : Add 5s to timer

## configuration ##
Variables used to change the IPTClock is positioned in Config/config.py

Further, changes to the fight layout in the form of stages and time can
be changed in the file stages.txt

 
## Build instructions ##
The pre built packages is constructed by using cx_Freeze to "freeze" the present
build and creates a separate python environment that can run the program.
You have to perform the building on the operating system you want the build for.
If you use exotic linux builds I can't predict the result ;-)

The built process is started by typing this in the terminal:

python3 setup.py build

Where python3 might be any desired python3 version.
(although see "Known bugs" for some version recommendation)

After build you might have to copy the folder and files containing configurations
to position relative the executable file in the build folder.
(for example stages.txt)


## Known bugs ##
I encountered a problem where the linking was broken while using cx_Freeze and
python 3.5, using python 3.4 solved this issue.


- Crashes on Mac OS X 10.10.5 when using dead keys. For details see issue #1 https://github.com/AlbinJS/IPTClock/issues/1

Present solution: Don't push dead keys on Mac OSX.


- Fullscreen on Mac doesn't use the area of the menus at the top and bottom.


- When exiting IPTClock on windows a pop telling python has stopped working.


- Resizing sponsor area using keybinds doesn't work in fullscreen on Windows.