#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################################
#  IPTClock, a graphical countdown clock for use with the international physicist's tournament
#    Copyright (C) 2016-2017  Albin Jonasson Svärdsby & Joel Magnusson
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################################



#########################
# Written in python 3,
# will exit for lower verions
##########################

#######################
# Import dependencies #
#######################

# check tkversion
# Import packages, and check for python version
import sys
if sys.version_info[0] < 3:
    print('You are using a Python version < 3 !! \n Functionality crippled!\n ')
    sys.exit(0)
else:
    import tkinter as tk
    import _thread # in order to utilize threads # the threading that is used is written for python 3
    usePython3 = True


# check os
usingLinuxMasterRace = False
usingWindows = False
usingMac = False
from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
    # LINUX
   usingLinuxMasterRace = True
elif _platform == "darwin":
   # MAC OS X
    usingMac = True
elif _platform == "win32":
   # Windows
    usingWindows = True


from tkinter import messagebox
#from tkinter import simpledialog
import tkinter.simpledialog as simpledialog

# import tkfont #to change font #NOT IMPLEMENTED

# imports the matplotlib and set variable installedMatplotlib
installedMatplotlib = True

import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import math
import time

# check if we use audio or not (.wave format)
try:
    import pyaudio
    installedPyaudio = True
except ImportError:
    installedPyaudio = False

if installedPyaudio:
    import wave


####################
# Global Variables #
####################
fps = 1

# Blue: '#7DC7EE'
# Yellow: '#FED812', '#eded1e'
# Red: '#d32c2c'
# Purple: '#864da0'
defaultBackgroundColor = None  # 'blue'    # String, following tkinter naming. color used for background, buttons and labels etc. NOT color behind wedge, use "None" without "" to get system default
wedgeBackgroundColor = None  # '#13235b' #String, following matplotlib naming.  color of the wedge background (for example to adhere to present year's color scheme. None defaults to Tkinter color from defaultBackgroundColor
clockColors = ['#7DC7EE', '#eded1e', '#d32c2c', '#864da0']  # List of colors for the clock to cycle through

# leftSponsImagePath = 
leftSponsImagePath = './ponyAndDuck.gif' # './Albin-300x286.gif'

pathToSoundFile = './theDuckSong2.wav'  # If left empty nothing happens

stagesPath = "./stages.txt"

# To be introduced...:
# defaultFont = # string deciding the standard font
# defaultFontSize =  # integer, fontsize of text


###################
# Import Settings #
###################
def import_stages():
    settings = open(stagesPath).read()
    separator = ' -- '
    if settings is not '':
        lines = [line.split(separator) for line in settings.split('\n')]
        stages = []
        for lineNbr, line in enumerate(lines):
            try:
                stage_time = int(line[0])
                stage_description = line[1]
                stages.append((stage_description, stage_time))
            except ValueError:
                pass
            except IndexError:
                pass
        return stages


#######################
# ClockGraphics Class #
#######################
class ClockGraphics:
    def __init__(self):
        # Definition of initial clock state/position
        self._clock_center = [0, 0]
        self._clock_reference_angle = 90
        self._clock_radius = 0.9
        self._angle = 0

        # Creation of clock graphical elements
        self._ax, self._fig, self._canvas = create_clock_canvas()
        self._wedge = self._create_wedge(2)
        self._backgroundDisc = self._create_circle(1, True)
        self._perimiterCircle = self._create_circle(3, False)

        # Dependable settings. Should later be set through kwargs.
        self._colors = [wedgeBackgroundColor] + clockColors  # [wedgeBackgroundColor, wedgeColor, 'red', 'purple']

        # Reset the clock
        self.reset()

    def _create_wedge(self, zorder):
        wedge = mpl.patches.Wedge(self._clock_center, self._clock_radius, self._clock_reference_angle, self._clock_reference_angle, zorder=zorder)
        self._ax.add_patch(wedge)
        return wedge

    def _create_circle(self, zorder, fill):
        circle = mpl.patches.Circle(self._clock_center, self._clock_radius, fill=fill, zorder=zorder)
        self._ax.add_patch(circle)
        return circle

    def _isTwelve(self):
        return abs(self._angle) % 360 < 1e-3 or 360 - abs(self._angle) % 360 < 1e-3

    def _update_wedge(self):
        if self._isTwelve():
            self._wedge.set_theta1(self._clock_reference_angle - 1e-3)
        else:
            self._wedge.set_theta1(self._clock_reference_angle + self._angle)

    def _updateCanvas(self):
        # Tkinter need to redraw the canvas to actually show the new updated matplotlib figure
        self._canvas.draw()

    def _switch_colors(self):
        lap = int(abs(self._angle - 1e-3)/360)
        if lap < len(self._colors)-1:
            wedge_color = self._colors[lap+1]
            background_color = self._colors[lap]
        else:
            wedge_color = self._backgroundDisc.get_facecolor()
            background_color = self._wedge.get_facecolor()
        self._wedge.set_facecolor(wedge_color)
        self._backgroundDisc.set_facecolor(background_color)

    def set_angle(self, new_angle):
        self._angle = new_angle
        self.update()

    def update(self):
        if self._isTwelve():
            self._switch_colors()
        self._update_wedge()
        self._updateCanvas()

    def reset(self):
        self.set_angle(0)


###############
# Timer Class #
###############
class Timer:
    def __init__(self):
        self._tick_state = False
        self._start_time = 0
        self._time = 0
        self._string = ''

        self._string_pattern = '{0:02d}:{1:02d}'  # the pattern format for the timer to ensure 2 digits
        self._time_step = 1/fps

        self.set_timer(self._start_time)

    def _update_string(self):
        seconds = int(abs(math.ceil(self._time - 1e-3)) % 60)
        minutes = int(abs(math.ceil(self._time - 1e-3)) // 60)
        # fixes the countdown clock when deadline is passed
        if self._time < 0:
                self._string = '-' + self._string_pattern.format(minutes, seconds)
        else:
            self._string = self._string_pattern.format(minutes, seconds)

    def _set_time(self, time):
        self._time = time
        self._update_string()

    def start_time(self):
        return self._start_time

    def time(self):
        return self._time

    def string(self):
        return self._string

    def set_timer(self, start_time):
        self._start_time = start_time
        self.reset()

    def tick(self):
        self._set_time(self._time-self._time_step)

    def isTicking(self):
        return self._tick_state

    def start(self):
        self._tick_state = True

    def pause(self):
        self._tick_state = False

    def reset(self):
        self._tick_state = False
        self._set_time(self._start_time)


###############
# Stage Class #
###############
class Stage:
    def __init__(self):
        self._stages = import_stages()
        self._nStages = len(self._stages)
        self._current_stage = 0

    def get(self):
        return self._current_stage

    def set(self, stage_number):
        self._current_stage = stage_number

    def description(self):
        return self._stages[self._current_stage][0]

    def time(self):
        return self._stages[self._current_stage][1]

    def next(self):
        if self._current_stage < self._nStages-1:
            self._current_stage += 1

    def previous(self):
        if self._current_stage > 0:
            self._current_stage -= 1

    def get_stages(self):
        return self._stages.copy()


###############
# Clock Class #
###############
class Clock:
    def __init__(self):
        self.stage = Stage()
        self.timer = Timer()
        self.clock_graphics = ClockGraphics()
        self.startPlayingSongTime = 55 # time in seconds when death mode sound is played

        self.challengeTimeLabel, self.countdownText, self.presentationTextLabel = create_clock_labels()

        self._update_stage_dependencies()

    # To start the countdown
    def start(self):
        self.timer.start()

    # To pause the countdown
    def pause(self):
        self.timer.pause()

    # To reset the countdown to startTime
    def reset(self):
        # reset the timer
        self.timer.reset()

        # Update the countdownText Label with the updated time
        self.countdownText.configure(text=self.timer.string())

        # reset the clock graphics
        self.clock_graphics.reset()

    # function updating the time
    def update(self):
        # Every time this function is called,
        # decrease timer with one second
        t0 = time.time()
        if self.timer.isTicking():
            self.timer.tick()

            # Update the countdownText Label with the updated time
            self.countdownText.configure(text=self.timer.string())

            # Update the clock graphics. Clock starts at 0 then negative direction clockwise
            angle = -360 * ((self.timer.start_time() - self.timer.time()) / self.timer.start_time())
            self.clock_graphics.set_angle(angle)

            # check for countdown time for activating "low health mode"
            if self.timer.time() == self.startPlayingSongTime:
                _thread.start_new_thread(PlayASoundFile, (pathToSoundFile,))

        # Call the update() function after 1/fps seconds
        dt = (time.time() - t0) * 1000
        time_left = max(0, int(1000 / fps - dt))
        master.after(time_left, self.update)

    def set_stage(self, stage_number):
        self.stage.set(stage_number)
        self._update_stage_dependencies()

    def previous_stage(self):
        self.stage.previous()
        self._update_stage_dependencies()

    def next_stage(self):
        self.stage.next()
        self._update_stage_dependencies()

    def _update_stage_dependencies(self):
        self.timer.set_timer(self.stage.time())

        self.countdownText.configure(text=self.timer.string())
        self.challengeTimeLabel.configure(text=self.timer.string())
        self.reset()
        self.presentationTextLabel.configure(text=self.stage.description())  # update text presenting stage


###################
# Sound Functions #
###################
def PlayASoundFile(pathToSoundFile):
    CHUNK = 64  # 1024
    wf = wave.open(pathToSoundFile, 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()


###########################
# Animated GIFs Functions #
###########################


###################
# Button Commands #
###################
# emphasise quit()
def _quit():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit(0)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit(0)


# toggling Fullscreen
def toogleFullscreen():
    global master, fullscreenButton
    state = not master.fullscreen
    master.attributes('-fullscreen', state)
    master.focus_set()
    master.fullscreen = state


def toogleFullscreenButton():
    global master, fullscreenButton
    state = not master.fullscreen
    master.attributes('-fullscreen', state)
    master.focus_set()
    master.fullscreen = state
    if (master.fullscreen):
        fullscreenButton.configure(text="Windowed")
    else:
        fullscreenButton.configure(text="Fullscreen")


def endFullscreen():
    global master
    master.fullscreen = False
    master.attributes("-fullscreen", False)
    master.focus_set()


def EditReporter():
    reporterString = simpledialog.askstring('Edit Reporter', 'Reporter', initialvalue=reporterNameLabel.cget('text'))
    reporterNameLabel.configure(text=reporterString)


def EditOpponent():
    opponentString = simpledialog.askstring('Edit Opponent', 'Opponent', initialvalue=opponentNameLabel.cget('text'))
    opponentNameLabel.configure(text=opponentString)


def EditReviewer():
    reviewerString = simpledialog.askstring('Edit Reviewer', 'Reviewer', initialvalue=reviewerNameLabel.cget('text'))
    reviewerNameLabel.configure(text=reviewerString)


#################
# GUI Functions #
#################
def create_clock_labels():
    # Digital clock present time
    challengeTimeLabel = tk.Label(master, text='', font=('Courier New', 26))
    challengeTimeLabel.grid(row=9, column=2, columnspan=3, rowspan=1)
    challengeTimeLabel.configure(background=defaultBackgroundColor)

    # Digital clock countdown
    countdownText = tk.Label(master, text='', font=('Courier New', 46))
    countdownText.grid(row=2, column=2, columnspan=3)
    countdownText.configure(background=defaultBackgroundColor)

    # Presentation of current phase
    presentationTextLabel = tk.Label(master, text='', font=('Courier New', 32))
    presentationTextLabel.grid(row=7, column=2, columnspan=3)
    presentationTextLabel.configure(background=defaultBackgroundColor)
    return challengeTimeLabel, countdownText, presentationTextLabel


def create_clock_canvas():
    fig = plt.figure(figsize=(16, 16), edgecolor=None, facecolor=wedgeBackgroundColor)

    ax = fig.add_subplot(111)
    ax.set_axis_bgcolor(None)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect(1)  # similar to "axis('equal')", but better.
    ax.axis('off')  # makes axis borders etc invisible.

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.show()
    canvas.get_tk_widget().grid(row=3, column=2, columnspan=3, rowspan=1)  # , sticky=tk.N)
    return ax, fig, canvas


def DoNothing():
    # Dummy function that does nothing
    pass



###################
# GUI Definitions #
###################
master = tk.Tk()  # define master tk object

DoNothing()
# fix icon on window
if usingWindows:
    master.iconbitmap(default='./Images/Ico/newIPTlogo_without_text.ico')

elif usingLinuxMasterRace:
    img = tk.PhotoImage(file='./Images/Ico/newIPTlogo_without_text.png')
    master.tk.call('wm', 'iconphoto', master._w, img)

elif usingMac:
    pass # does nothing

else:
    pass

# change window title
master.wm_title("IPTClock")

# bindings for fullscreen
master.fullscreen = False
master.attributes('-fullscreen', False)
master.bind("<F11>", toogleFullscreen)
master.bind("<Escape>", endFullscreen)

# set the background color, given from variable at start
master.configure(background=defaultBackgroundColor)

# Find default background color and check in case we use it
defaultbgColor = master.cget('bg')  # find system window default color
bgRGB = master.winfo_rgb(defaultbgColor)
bgRGB = (bgRGB[0]/(256**2), bgRGB[1]/(256**2), bgRGB[2]/(256**2))

if wedgeBackgroundColor is None:
    wedgeBackgroundColor = bgRGB

# boolean for fullscreen
master.fullscreen = False


#################
# Sponsor Image #
#################

sponsImage = tk.PhotoImage(file=leftSponsImagePath)

sponsLabel = tk.Label(master, image=sponsImage)
sponsLabel.grid(row=0, column=0, columnspan=1, rowspan=9)


####################
# Competitor Names #
####################
# Reporter
reporterLabel = tk.Label(master, text="Reporter:", font=('Courier New', 16))
reporterLabel.grid(row=11, column=2)
reporterLabel.configure(background=defaultBackgroundColor)
reporterNameLabel = tk.Label(master, text='', font=('Courier New', 16))
reporterNameLabel.grid(row=11, column=3)

# Opponent
opponentLabel = tk.Label(master, text="Opponent:", font=('Courier New', 16))
opponentLabel.grid(row=12, column=2)
opponentLabel.configure(background=defaultBackgroundColor)
opponentNameLabel = tk.Label(master, text='', font=('Courier New', 16))
opponentNameLabel.grid(row=12, column=3)

# Reviewer
reviewerLabel = tk.Label(master, text="Reviewer:", font=('Courier New', 16))
reviewerLabel.grid(row=13, column=2)
reviewerLabel.configure(background=defaultBackgroundColor)
reviewerNameLabel = tk.Label(master, text='', font=('Courier New', 16))
reviewerNameLabel.grid(row=13, column=3)

####################
# Initialize Clock #
####################
IPTClock = Clock()


###################
# Control Buttons #
###################
# Start Button
startButton = tk.Button(master=master, text='Start', command=IPTClock.start)
startButton.grid(row=4, column=6, sticky='WE')
startButton.configure(background=defaultBackgroundColor)

# Pause Button
pauseButton = tk.Button(master=master, text='Pause', command=IPTClock.pause)
pauseButton.grid(row=5, column=6, sticky='WE')
pauseButton.configure(background=defaultBackgroundColor)

# Reset button
resetButton = tk.Button(master=master, text='Reset', command=IPTClock.reset)
resetButton.grid(row=11, column=6, sticky='WE')
resetButton.configure(background=defaultBackgroundColor)

# Quit button
quitButton = tk.Button(master=master, text='Quit', command=_quit)
quitButton.grid(row=13, column=6, sticky='WE')
quitButton.configure(background=defaultBackgroundColor)

# Fullscreen
fullscreenButton = tk.Button(master=master, text='Fullscreen', command=toogleFullscreenButton)
fullscreenButton.grid(row=7, column=6, sticky='WE')
fullscreenButton.configure(background=defaultBackgroundColor)

# Edit Reporter
editReporterButton = tk.Button(master=master, text='Edit', command=EditReporter)
editReporterButton.grid(row=11, column=4)
editReporterButton.configure(background=defaultBackgroundColor)

# Edit Opponent
editOpponentButton = tk.Button(master=master, text='Edit', command=EditOpponent)
editOpponentButton.grid(row=12, column=4)
editOpponentButton.configure(background=defaultBackgroundColor)

# Edit Reviewer
editReviewerButton = tk.Button(master=master, text='Edit', command=EditReviewer)
editReviewerButton.grid(row=13, column=4)
editReviewerButton.configure(background=defaultBackgroundColor)

# Previous Stage
previousStageButton = tk.Button(master=master, text='<<', command=IPTClock.previous_stage)
previousStageButton.grid(row=8, column=6, sticky='WE')

# Next Stage
nextStageButton = tk.Button(master=master, text='>>', command=IPTClock.next_stage)
nextStageButton.grid(row=9, column=6, sticky='WE')


#####################
# layout lines
####################

horizontalLine = tk.Label(master, text='-', background='darkgray', height=1, font=('Courier New', 1), borderwidth=0)
horizontalLine.grid(row=10, column=2, columnspan=3, sticky='WE')

verticalLineRight = tk.Label(master, text='-', background='darkgray', height=1, font=('Courier New', 1), borderwidth=0)
verticalLineRight.grid(row=0, column=5, columnspan=1, rowspan=14, sticky='NS')

verticalLineLeft = tk.Label(master, text='-', background='darkgray', height=1, font=('Courier New', 1), borderwidth=0)
verticalLineLeft.grid(row=0, column=1, columnspan=1, rowspan=14, sticky='NS')


##########################
# Top menu configuration #
##########################

menubar = tk.Menu(master)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_separator()

filemenu.add_command(label="Exit", command=_quit)
menubar.add_cascade(label="File", menu=filemenu)


# drop down menu to chose stage
stagemenu = tk.Menu(menubar, tearoff=0)
for i, stage in enumerate(IPTClock.stage.get_stages()):
    stagemenu.add_command(label=str(i) + ": " + stage[0],
                          command=lambda stage_number=i: IPTClock.set_stage(stage_number))

menubar.add_cascade(label="Stage", menu=stagemenu)


# help menu
logo_image = tk.PhotoImage(file='./Images/IPTlogos/newIPTlogo_without_text.gif') # needed outside aboutPopup to avoid garbage collect

# about this application
def AboutPopup():
    # creates a popup window showing basic info and copywright
    top_about = tk.Toplevel()
    top_about.title("About IPTClock")

#    logo_image = tk.PhotoImage(file='./Images/IPTlogos/newIPTlogo_without_text.gif')
    about_logo=tk.Label(top_about, image=logo_image)
    about_logo.pack(side='left')
    
    about_message = "IPTClock is a countdown clock written for use in the International Physicist's Tournament. The program is written using Python 3 with Tkinter and matplotlib.\n\n Copyright (c) 2016-2017 by Albin Jonasson Svärdsby  \n Joel Magnusson"    
    about_msg = tk.Message(top_about, text=about_message)
    about_msg.pack(side='right')

    about_exit_button = tk.Button(top_about, text="Dismiss", command=top_about.destroy)
    about_exit_button.pack(side='bottom')


helpmenu = tk.Menu(menubar, tearoff=0) # create helpmenu
helpmenu.add_command(label="About", command= AboutPopup )

menubar.add_cascade(label="Help", menu=helpmenu) # add helpmenu

master.config(menu=menubar) # set the final menu

# change column behaviour for scaling
master.columnconfigure(3, weight=1)
master.rowconfigure(3, weight=1)


IPTClock.update()  # update the countdown

master.protocol("WM_DELETE_WINDOW", on_closing)  # necessary to cleanly exit the program when using the windows manager

# start the GUI loop
master.mainloop()
