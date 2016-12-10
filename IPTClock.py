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


######################################
# Global Variables, change each year #
######################################

presentationText = "IPT 2017 Göteborg"  # should be string, text that shows at start
defaultBackgroundColor = None  # 'blue'    # String, following tkinter naming. color used for background, buttons and labels etc. NOT color behind wedge, use "None" without "" to get system default
wedgeBackgroundColor = None  # '#13235b' #String, following matplotlib naming.  color of the wedge background (for example to adhere to present year's color scheme. None defaults to Tkinter color from defaultBackgroundColor

wedgeColor = '#ffe000'  # String, following matplotlib naming. color of the wedge (for example to adhere to present year's color scheme
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

    global countdownTime  # variable containing seconds left
    global countdownState
   
    # Every time this function is called, 
    # decrease countdownTime with one second

    if countdownTime <= 0:
        wedge.set_facecolor('red')  # change background disc color when countdown becomes negative
        backgroundDisc.set_facecolor(wedgeColor)

    if countdownState:
        countdownTime -= 1
        # run the functions updating the graphical representation
        update_countdownText()
        update_angle()
        
        # check for countdown time for activating "low health mode"
        if countdownTime == 55:
            _thread.start_new_thread(PlayASoundFile, (pathToSoundFile,) )

    # Call the update_countdown() function after 1 second
    master.after(1000, update_countdown)  # wait 1000 [ms]


# function updating the presented digital countdown
def update_countdownText():
    if (countdownState):
        global countdownTime  # variable containing seconds left
             
        # create string for countdownTimer
        timerSeconds = abs(countdownTime) % 60
        timerMinutes = abs(countdownTime) // 60
        
        # fixes the countdown clock when deadline is passed
        if countdownTime < 0:
                if timerMinutes > 0:
                        timeString = pattern.format(-timerMinutes, timerSeconds)
                else:
                        timeString = pattern.format(timerMinutes, -timerSeconds)
        else:
            timeString = pattern.format(timerMinutes, timerSeconds)
        # Update the countdownText Label with the updated time
        countdownText.configure(text=timeString)


# Function updating and drawing the "pie wedge" for the countdown
def update_angle():
    if (countdownState):
        global countdownTime, countdownStartTime

        # if countdownTime%2 > 0: # in case draw is taxing

        # angle starts at 90 then negative direction clockwise
        angle = 90 - 360 * ((countdownStartTime-countdownTime)/countdownStartTime)
        currentAngle = angle
        update_wedgeAx(wedgeAx, currentAngle)
        updateWedgeCanvas(wedgeCanvas)  # call tkinter to redraw the canvas


###################
# Button Commands #
###################
    
# To start the countdown
def StartCountdown():
    global countdownState
#    ResetCountdown
    countdownState = True


# To pause the countdown
def PauseCountdown():
    global countdownState
    countdownState = False


# To reset the countdown to startTime
def ResetCountdown():
    global countdownTime, countdownStartTime, countdownState
    countdownTime = countdownStartTime 
    countdownState = False
    
    # create string for countdownTimer
    timerSeconds = countdownTime % 60
    timerMinutes = countdownTime // 60
        
    timeString = pattern.format(timerMinutes, timerSeconds)
    # Update the countdownText Label with the updated time
    countdownText.configure(text=timeString)

    # update the wedge on canvas
    currentAngle = 90
    wedge.set_facecolor(wedgeColor)
    backgroundDisc.set_facecolor(wedgeBackgroundColor)
    update_wedgeAx(wedgeAx, currentAngle)
    updateWedgeCanvas(wedgeCanvas)  # call tkinter to redraw the canvas


# emphasise quit()
def _quit():
    sys.exit(0)  # shuts down entire python script


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit(0)


########################
# matplotlib Functions #
########################
def initialize_figure(wedgeBackgroundColor):
    # figsize is used to make sure the countdown wedge is large enough. If you find it to small, increase the figsize.
    wedgeFig = plt.figure(figsize=(16, 16), edgecolor=None, facecolor=wedgeBackgroundColor)
    wedgeAx = wedgeFig.add_subplot(111)
    wedgeCanvas = FigureCanvasTkAgg(wedgeFig, master=master)
    wedgeCanvas.show()
    wedgeCanvas.get_tk_widget().grid(row=0, column =2, columnspan=3, rowspan= 3, sticky=tk.N)
    return wedgeFig, wedgeAx, wedgeCanvas


def set_wedgeAx_settings(wedgeAx):
    wedgeAx.set_axis_bgcolor(None)
    wedgeAx.set_xlim(-1, 1)
    wedgeAx.set_ylim(-1, 1)

    wedgeAx.set_aspect(1)   # similar to "axis('equal')", but better.
    wedgeAx.axis('off')     # makes axis borders etc invisible. Comment out the current line if you want to compare set_aspect to axis('equal')


def initialize_wedge(wedgeAx, wedgeColor, zOrder):
    # simply creates a wedge and return handle
    startPos = [0, 0]
    startAngle = 90
    R = 0.9

    wedge = mpl.patches.Wedge(startPos, R, startAngle, startAngle, facecolor=wedgeColor, zorder=zOrder)
    wedgeAx.add_patch(wedge)
    return wedge


def initialize_circle(wedgeAx, filledCircle, zOrder, circleColor):
        # simply creates a circle or disc and returns handle
        startPos = [0, 0]
        R = 0.9
        perimeterCircle = mpl.patches.Circle(startPos, R, fill=filledCircle, zorder=zOrder, facecolor= circleColor)
        wedgeAx.add_patch(perimeterCircle)
        return perimeterCircle

        
def update_wedgeAx(wedgeAx, currentAngle):
    # updates the wedges in wedgeAx with respect to angle
    wedges = [patch for patch in wedgeAx.patches if isinstance(patch, mpl.patches.Wedge)]
    wedge = wedges[-1]
    wedge.set_theta1(currentAngle)


def updateWedgeCanvas(wedgeCanvas):
        # Tkinter need to redraw the canvas to actually show the new updated matplotlib figure
        wedgeCanvas.draw()

                        
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
    countdownStartTime = stages[stageNumber][1]
    SetCountdownStage(countdownStartTime)  # make the time adjustment
    presentationTextLabel.configure(text=titleText)  # update text presenting stage


def SetCountdownStage(countdownStartTimeInput):
    global countdownState, countdownStartTime, countdownTime
    countdownState = False  # Reassuring
    countdownStartTime = countdownStartTimeInput
    countdownTime = countdownStartTime
    timerSeconds = countdownStartTime % 60
    timerMinutes = countdownStartTime // 60
    
    timeString = pattern.format(timerMinutes, timerSeconds)
    # Update the countdownText Label with the updated time
    countdownText.configure(text=timeString)
    challengeTimeLabel.configure(text=timeString)
    
    # update the wedge on canvas
    ResetCountdown()


countdownState = False  # set start state of timer to false.
countdownStartTime = 10  # initialise


###################
# GUI Definitions #
###################
master = tk.Tk()  # define master tk object

countdownTime = countdownStartTime
pattern = '{0:02d}:{1:02d}'  # the pattern format for the timer to ensure 2 digits

# set the background color, given from variable at start
master.configure(background=defaultBackgroundColor)

# Find default background color and check in case we use it
defaultbgColor = master.cget('bg')  # find system window default color
bgRGB = master.winfo_rgb(defaultbgColor)
bgRGB = (bgRGB[0]/(256**2), bgRGB[1]/(256**2), bgRGB[2]/(256**2))

if wedgeBackgroundColor is None:
        wedgeBackgroundColor = bgRGB


#################
# Sponsor Image #
#################

sponsImage = tk.PhotoImage(file=leftSponsImagePath)

sponsLabel = tk.Label(master, image=sponsImage)
sponsLabel.grid(row=0, column=0, columnspan=2, rowspan=2)


####################
# Competitor Names #
####################
# add fields for reporter etc.
# Reporter
reporterLabel = tk.Label(master, text="Reporter", font=('Courier New', 16))
reporterLabel.grid(row=6, column=0)
reporterLabel.configure(background=defaultBackgroundColor)

reporterStringVar = tk.StringVar()
reporterEntry = tk.Entry(master, bd=5, width=24, textvariable=reporterStringVar, font=('Courier New', 16))
reporterEntry.grid(row=6, column=1)
reporterEntry.configure(background=defaultBackgroundColor)

# Opponent
opponentLabel = tk.Label(master, text="Opponent", font=('Courier New', 16))
opponentLabel.grid(row=7, column=0)
opponentLabel.configure(background=defaultBackgroundColor)

opponentStringVar = tk.StringVar()
opponentEntry = tk.Entry(master, bd=5, width=24, textvariable=opponentStringVar, font=('Courier New', 16))
opponentEntry.grid(row=7, column=1)
opponentEntry.configure(background=defaultBackgroundColor)

# Reviewer
reviewerLabel = tk.Label(master, text="Reviewer", font=('Courier New', 16))
reviewerLabel.grid(row=8, column=0)
reviewerLabel.configure(background=defaultBackgroundColor)

reviewerStringVar = tk.StringVar()
reviewerEntry = tk.Entry(master, bd=5, width=24, textvariable=reviewerStringVar, font=('Courier New', 16))
reviewerEntry.grid(row=8, column=1)
reviewerEntry.configure(background=defaultBackgroundColor)


#################################
# Initialize matplotlib objects #
#################################
# call matplotlib for initial setup
currentAngle = 90

wedgeFig, wedgeAx, wedgeCanvas = initialize_figure(wedgeBackgroundColor)
set_wedgeAx_settings(wedgeAx)
zOrderWedge = 2
wedge = initialize_wedge(wedgeAx, wedgeColor, zOrderWedge)

# background plate
zOrderCircle = 1
circleFilled = True
backgroundDisc = initialize_circle(wedgeAx, circleFilled, zOrderCircle, wedgeBackgroundColor)
# perimiter circle
zOrderCircle2 = 3
circleFilled = False
perimiterCircle = initialize_circle(wedgeAx, circleFilled, zOrderCircle2, 'black')
update_wedgeAx(wedgeAx, currentAngle)
    
#####################
# frame for bottoms and writing, (at the bottom and right
##################
# create string for countdownTimer startTime
timerSeconds = countdownStartTime % 60
timerMinutes = countdownStartTime // 60        
timeString = pattern.format(timerMinutes, timerSeconds)


# Digital clock present time
# challengeTimeVar = "01:00" # this should be coupled to choice of stage
challengeTimeVar = timeString
challengeTimeLabel = tk.Label(master, text=challengeTimeVar, font=('Courier New', 18))
challengeTimeLabel.grid(row=8, column=3, rowspan=2)
challengeTimeLabel.configure(background=defaultBackgroundColor)

challengeTimeTextLabel = tk.Label(master, text="ChallengeTime", font=('Courier New', 18))
challengeTimeTextLabel.grid(row=6, column=3, rowspan=2)
challengeTimeTextLabel.configure(background=defaultBackgroundColor)


# Digital clock countdown
digitalCountdownVar = timeString
countdownText = tk.Label(master, text=digitalCountdownVar, font=('Courier New', 18))
countdownText.grid(row=8, column=4, rowspan=2)
countdownText.configure(background=defaultBackgroundColor)

countdownTextLabel = tk.Label(master, text="Countdown", font=('Courier New', 18))
countdownTextLabel.grid(row=6, column=4, rowspan=2)
countdownTextLabel.configure(background=defaultBackgroundColor)


# Presentation of current phase
presentationTextLabel = tk.Label(master, text=presentationText, font=('Courier New', 28))
presentationTextLabel.grid(row=4, column=2, columnspan=2)
presentationTextLabel.configure(background=defaultBackgroundColor)


###################
# Control Buttons #
###################
# StartButton
startButton = tk.Button(master=master, text='Start', command=StartCountdown)
startButton.grid(row=5, column=7)
startButton.configure(background=defaultBackgroundColor)

# PauseButton
pauseButton = tk.Button(master=master, text='Pause', command=PauseCountdown)
pauseButton.grid(row=6, column=7)
pauseButton.configure(background=defaultBackgroundColor)

# Reset button
resetButton = tk.Button(master=master, text='Reset', command=ResetCountdown)
resetButton.grid(row=6, column=8)
resetButton.configure(background=defaultBackgroundColor)

# Quit button
quitButton = tk.Button(master=master, text='Quit', command=_quit)
quitButton.grid(row=8, column=8)
quitButton.configure(background=defaultBackgroundColor)


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
master.columnconfigure(3, weight=1)
master.columnconfigure(3, pad=7)
master.columnconfigure(6, weight=1)
master.rowconfigure(0, weight=1)
master.rowconfigure(1, weight=1)
master.rowconfigure(4, pad=7)


update_countdown()  # update the countdown

master.protocol("WM_DELETE_WINDOW", on_closing)  # necessary to cleanly exit the program when using the windows manager
# start the GUI loop
master.mainloop()
