#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################
# IPTClock, a graphical countdown clock for use with the
# international physicist's tournament
#
# Written in python 3, will exit for lower verions
#
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


# check if we use audio or not (.wave format)
try:
    import pyaudio
    installedPyaudio = True
except ImportError:
    installedPyaudio = False

if installedPyaudio:
    import wave


# for converting and accepting more fileformats for photos, NOT IMPLEMENTED
# from PIL import Image, ImageTk

simulated_time_step = 10  # [ms]
######################################
# Global Variables, change each year #
######################################

presentationText = "IPT 2017 Göteborg"  # should be string, text that shows at start

defaultBackgroundColor = None  # 'blue'    # String, following tkinter naming. color used for background, buttons and labels etc. NOT color behind wedge, use "None" without "" to get system default
wedgeBackgroundColor = None  # '#13235b' #String, following matplotlib naming.  color of the wedge background (for example to adhere to present year's color scheme. None defaults to Tkinter color from defaultBackgroundColor
clockColors = ['#ffe000', 'red', 'purple']  # List of colors for the clock to cycle through

# leftSponsImagePath = './Albin-300x286.gif'
leftSponsImagePath = './ponyAndDuck.gif'

pathToSoundFile = './theDuckSong2.wav'  # 'allahu.wav' #'SaleelSawarimNasheed.wav' # If left empty nothing happens


# To be introduced...:
# defaultFont = # string deciding the standard font
# defaultFontSize =  # integer, fontsize of text


####################
# Update Functions #
####################

# function updating the time
def update_countdown():
    # Every time this function is called, 
    # decrease timer with one second
    if timer.isTicking():
        timer.tick()

        # Update the countdownText Label with the updated time
        countdownText.configure(text=timer.string())

        # Update the clock graphics. Clock starts at 0 then negative direction clockwise
        angle = -360 * ((timer.start_time() - timer.time()) / timer.start_time())
        clock.set_angle(angle)
        
        # check for countdown time for activating "low health mode"
        if timer.time() == 55:
            _thread.start_new_thread(PlayASoundFile, (pathToSoundFile,))

    # Call the update_countdown() function after 1 second
    master.after(simulated_time_step, update_countdown)  # wait 1000 [ms]


###################
# Button Commands #
###################
    
# To start the countdown
def StartCountdown():
    timer.start()


# To pause the countdown
def PauseCountdown():
    timer.pause()


# To reset the countdown to startTime
def ResetCountdown():
    # reset the timer
    timer.reset()

    # Update the countdownText Label with the updated time
    countdownText.configure(text=timer.string())

    # reset the clock
    clock.reset()


# emphasise quit()
def _quit():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit(0)
#    sys.exit(0)  # shuts down entire python script
  

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit(0)


# toggling Fullscreen
def toogleFullscreen(self):
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

  
def endFullscreen(self):
    global master
    master.fullscreen = False
    master.attributes("-fullscreen", False)
    master.focus_set()



def EditReporter():
   # reporterString=tk.simpledialog.askstring('Edit Reporter', prompt , initialvalue= 'Arnold Schwarzenegger' )
#    tkinter.simpledialog
     reporterString=simpledialog.askstring('Edit Reporter', 'Reporter' , initialvalue= 'Arnold Schwarzenegger' )
     reporterNameLabel.configure(text = reporterString)


    
###############
# Clock Class #
###############

#######################
# ClockGraphics Class #
#######################

class ClockGraphics:
    def __init__(self):
        # Definition of initial clock state/position
        self._clock_center = [0, 0]
        self._clock_reference_angle = 30
        self._clock_radius = 0.9
        self._angle = 0

        # Creation of clock graphical elements
        self._ax, self._fig, self._canvas = self._create_canvas()
        self._wedge = self._create_wedge(2)
        self._backgroundDisc = self._create_circle(1, True)
        self._perimiterCircle = self._create_circle(3, False)

        # Dependable settings. Should later be set through kwargs.
        self._colors = [wedgeBackgroundColor] + clockColors  # [wedgeBackgroundColor, wedgeColor, 'red', 'purple']

        # Reset the clock
        self.reset()

    def _create_canvas(self):
        fig = plt.figure(figsize=(16, 16), edgecolor=None, facecolor=wedgeBackgroundColor)

        ax = fig.add_subplot(111)
        ax.set_axis_bgcolor(None)
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_aspect(1)  # similar to "axis('equal')", but better.
        ax.axis('off')  # makes axis borders etc invisible.

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.show()
        canvas.get_tk_widget().grid(row=3, column=1, columnspan=3, rowspan=1)  # , sticky=tk.N)
        return ax, fig, canvas

    def _create_wedge(self, zOrder):
        wedge = mpl.patches.Wedge(self._clock_center, self._clock_radius, self._clock_reference_angle, self._clock_reference_angle, zorder=zOrder)
        self._ax.add_patch(wedge)
        return wedge

    def _create_circle(self, zOrder, fill):
        circle = mpl.patches.Circle(self._clock_center, self._clock_radius, fill=fill, zorder=zOrder)
        self._ax.add_patch(circle)
        return circle

    def _update_wedge(self):
        if self._angle % 360 == 0:
            self._wedge.set_theta1(self._clock_reference_angle - 0.001)
        else:
            self._wedge.set_theta1(self._clock_reference_angle + self._angle)

    def _updateCanvas(self):
        # Tkinter need to redraw the canvas to actually show the new updated matplotlib figure
        self._canvas.draw()

    def _switch_colors(self):
        lap = int(abs(self._angle)//360)
        if lap < len(self._colors)-1:
            wedge_color = self._colors[lap+1]
            background_color = self._colors[lap]
        else:
            wedge_color = self._backgroundDisc.get_facecolor()
            background_color = self._wedge.get_facecolor()
        self._wedge.set_facecolor(wedge_color)
        self._backgroundDisc.set_facecolor(background_color)

    def set_angle(self, newAngle):
        self._angle = newAngle
        self.update()

    def update(self):
        if abs(self._angle) % 360 == 0:
            self._switch_colors()
        self._update_wedge()
        self._updateCanvas()

    def reset(self):
        self.set_angle(0)


#######################
# Timer Class #
#######################
class Timer:
    def __init__(self):
        self._tick_state = False
        self._time = None
        self._string = None

        self._string_pattern = '{0:02d}:{1:02d}'  # the pattern format for the timer to ensure 2 digits
        self._time_step = 1
        self._start_time = 10

        self.set_timer(self._start_time)

    def _update_string(self):
        seconds = abs(self._time) % 60
        minutes = abs(self._time) // 60
        # fixes the countdown clock when deadline is passed
        if self._time < 0:
            if minutes > 0:
                self._string = self._string_pattern.format(-minutes, seconds)
            else:
                self._string = self._string_pattern.format(minutes, -seconds)
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


########################
# Definition of Stages #
########################
# Stage description and time in seconds
stages = [("The Opponent Challenges the Reporter", 1*60),
          ("The Reporter accepts or rejects the challenge", 2*60),
          ("Preparation of the Reporter", 5*60),
          ("Presentation of the report", 10*60),
          ("Questions from the opponent", 2*60),
          ("Preparation for the opponent", 3*60),
          ("The opponent's speech", 5*60),
          ("Discussion between the reporter and opponent", 5*60),
          ("Questions from the reviewer", 2*60),
          ("Preparation for the reviewer", 1*60),
          ("The reviewer's speech", 3*60),
          ("Discussion on stage", 4*60),
          ("General discussion between the teams", 5*60),
          ("Concluding remarks of the reporter", 1*60),
          ("Questions of the jury", 6*60),
          ("Putting marks", 1*60),
          ("Jury remarks", 4*60)]


def SetStage(stageNumber):
    titleText = stages[stageNumber][0]
    timer.set_timer(stages[stageNumber][1])

    countdownText.configure(text=timer.string())
    challengeTimeLabel.configure(text=timer.string())
    ResetCountdown()
    presentationTextLabel.configure(text=titleText)  # update text presenting stage


###################
# GUI Definitions #
###################
master = tk.Tk()  # define master tk object

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
#master.bind("<F11>", toggle_fullscreen() )
#master.bind("<Escape>", end_fullscreen() )
#master.bind("<F11>", master.toggle_fullscreen)
#master.bind("<Escape>", master.end_fullscreen)        
        
#################
# Sponsor Image #
#################

sponsImage = tk.PhotoImage(file=leftSponsImagePath)

sponsLabel = tk.Label(master, image=sponsImage)
sponsLabel.grid(row=0, column=0, columnspan=1, rowspan=9)


####################
# Competitor Names #
####################
# add fields for reporter etc.
# Reporter
reporterLabel = tk.Label(master, text="Reporter", font=('Courier New', 16))
reporterLabel.grid(row=10, column=1)
reporterLabel.configure(background=defaultBackgroundColor)

reporterStringVar = tk.StringVar()
#reporterEntry = tk.Entry(master, bd=5, width=24, textvariable=reporterStringVar, font=('Courier New', 16))
reporterNameLabel = tk.Label(master, text= '', font=('Courier New', 16) )
reporterNameLabel.grid(row=10, column=2)
#reporterEntry.grid(row=10, column=2)
#reporterEntry.configure(background=defaultBackgroundColor)

# Opponent
opponentLabel = tk.Label(master, text="Opponent", font=('Courier New', 16))
opponentLabel.grid(row=11, column=1)
opponentLabel.configure(background=defaultBackgroundColor)

opponentStringVar = tk.StringVar()
opponentEntry = tk.Entry(master, bd=5, width=24, textvariable=opponentStringVar, font=('Courier New', 16))
opponentEntry.grid(row=11, column=2)
opponentEntry.configure(background=defaultBackgroundColor)

# Reviewer
reviewerLabel = tk.Label(master, text="Reviewer", font=('Courier New', 16))
reviewerLabel.grid(row=12, column=1)
reviewerLabel.configure(background=defaultBackgroundColor)

reviewerStringVar = tk.StringVar()
reviewerEntry = tk.Entry(master, bd=5, width=24, textvariable=reviewerStringVar, font=('Courier New', 16))
reviewerEntry.grid(row=12, column=2)
reviewerEntry.configure(background=defaultBackgroundColor)


####################
# Initialize Clock #
####################
timer = Timer()
clock = ClockGraphics()

#####################
# frame for bottoms and writing, (at the bottom and right
##################

# Digital clock present time
challengeTimeVar = timer.string()
challengeTimeLabel = tk.Label(master, text=challengeTimeVar, font=('Courier New', 26))

challengeTimeLabel.grid(row=9, column=1, columnspan=3,rowspan=1)
challengeTimeLabel.configure(background=defaultBackgroundColor)

#challengeTimeTextLabel = tk.Label(master, text="ChallengeTime", font=('Courier New', 18))
#challengeTimeTextLabel.grid(row=8, column=4, rowspan=2)
#challengeTimeTextLabel.configure(background=defaultBackgroundColor)


# Digital clock countdown
digitalCountdownVar = timer.string()
countdownText = tk.Label(master, text=digitalCountdownVar, font=('Courier New', 46))
countdownText.grid(row=2, column=1, columnspan=3)
countdownText.configure(background=defaultBackgroundColor)

#countdownTextLabel = tk.Label(master, text="Countdown", font=('Courier New', 18))
#countdownTextLabel.grid(row=1, column=7, rowspan=2)
#countdownTextLabel.configure(background=defaultBackgroundColor)


# Presentation of current phase
presentationTextLabel = tk.Label(master, text=presentationText, font=('Courier New', 32))
presentationTextLabel.grid(row=7, column=1, columnspan=3)
presentationTextLabel.configure(background=defaultBackgroundColor)


###################
# Control Buttons #
###################
# StartButton
startButton = tk.Button(master=master, text='Start', command=StartCountdown)
startButton.grid(row=4, column=4, sticky='WE' )
startButton.configure(background=defaultBackgroundColor)

# PauseButton
pauseButton = tk.Button(master=master, text='Pause', command=PauseCountdown)
pauseButton.grid(row=5, column=4, sticky='WE')
pauseButton.configure(background=defaultBackgroundColor)

# Reset button
resetButton = tk.Button(master=master, text='Reset', command=ResetCountdown)
resetButton.grid(row=10, column=4, sticky='WE')
resetButton.configure(background=defaultBackgroundColor)

# Quit button
quitButton = tk.Button(master=master, text='Quit', command=_quit)
quitButton.grid(row=12, column=4, sticky='WE')
quitButton.configure(background=defaultBackgroundColor)

# Fullscreen
fullscreenButton = tk.Button(master=master, text='Fullscreen', command=toogleFullscreenButton)
fullscreenButton.grid(row=7, column=4, sticky='WE')
fullscreenButton.configure(background=defaultBackgroundColor)


editReporterButton = tk.Button(master=master, text='Edit', command=EditReporter)
editReporterButton.grid(row=10, column=3)
editReporterButton.configure(background=defaultBackgroundColor)


#####################
# layout lines
####################

horizontalLine = tk.Label(master, text='-', foreground='black', background='black', height=1, font=('Courier New', 1), borderwidth = 0 )
horizontalLine.grid(row=9,column=1, columnspan=3, sticky='WE')


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
for stageNumber in range(len(stages)):
    stagemenu.add_command(label=str(stageNumber+1) + ":" + stages[stageNumber][0],
                          command=lambda stageNumber=stageNumber: SetStage(stageNumber))

menubar.add_cascade(label="Stage", menu=stagemenu)
master.config(menu=menubar)


# change column behaviour for scaling
#master.columnconfigure(0, weight=1)
#master.columnconfigure(2, weight=1)
#master.columnconfigure(3, pad=7)
master.columnconfigure(3, weight=1)
master.rowconfigure(3, weight=1)
#master.rowconfigure(0, weight=1)
#master.rowconfigure(4, pad=7)


update_countdown()  # update the countdown

master.protocol("WM_DELETE_WINDOW", on_closing)  # necessary to cleanly exit the program when using the windows manager
# start the GUI loop
master.mainloop()
