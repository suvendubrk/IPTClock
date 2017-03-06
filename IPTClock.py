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
    print('You are using a Python version < 3 !! \n Repent!\n ')
    sys.exit(0)
else:    
    import _thread # in order to utilize threads # the threading that is used is written for python 3
    usePython3 = True

# import tkinter    
import tkinter as tk
from tkinter import messagebox # used for popups
from tkinter import simpledialog
import tkinter.font as tkFont # used for custom font settings

import math
import time
    
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

# configuration variables
from Config.config import *

# import classes
from Classes.iptclock_classes import *

        
# function creating class and running update
def Timeout(clockHandle):    
    IPTTimeout = TimeoutClass(clockHandle)
    IPTTimeout.setupTimeout()
    IPTTimeout.update()


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
    toogleFullscreenButton()

def toogleFullscreenLinux(temp):
    toogleFullscreenButton() 

def toogleFullscreenButton():
    global master, fullscreenButton
    state = not master.fullscreen
    master.attributes('-fullscreen', state)
    master.focus_set()
    master.fullscreen = state
    if (master.fullscreen):
        fullscreenButton.configure(text="Windowed")
        master.fullscreenSwitch.set(True) # traced variable
        screenWidth = master.winfo_screenwidth() 
    else:
        fullscreenButton.configure(text="Fullscreen")
        master.fullscreenSwitch.set(False) # traced variable
        screenWidth = 640
    FontResize(screenWidth)

def endFullscreenLinux(tmp):
    endFullscreen() # there's some difference between os and input using keyes
    

def endFullscreen():
    global master, fullscreenButton
    master.fullscreen = False
    master.attributes("-fullscreen", False)
    fullscreenButton.configure(text="Fullscreen")
    master.focus_set()
    SponsImageResize() # needed since it might skip resizing back elsewise
    master.fullscreenSwitch.set(False) # traced variable
    time.sleep(3)
    FontResize()

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
def FontResize(screenWidthPixels):    
    # Determine present windowsize then upscale the font with the ration
    # between the present width and 480p (width 640 pixels) (choosen as base).
    # Uses original font sizes 

    #widthPix =  master.winfo_width()
    #widthPix =  master.winfo_screenwidth()
    widthPix = screenWidthPixels
    widthRatio = widthPix / 640.0
    
    fontSize = master.customFontCompetitors_orig
    fontSize = math.floor(fontSize*widthRatio)
    master.customFontCompetitors.configure(size=fontSize)

    fontSize = master.customFontButtons_orig
    fontSize = math.floor(fontSize*widthRatio)
    if (abs(fontSize) > 16):
        fontSize = 16
    master.customFontButtons.configure(size=fontSize)

    fontSize = master.customFontDigitalClock_orig
    fontSize = math.floor(fontSize*widthRatio)
    master.customFontDigitalClock.configure(size=fontSize)

    fontSize = master.customFontStage_orig
    fontSize = math.floor(fontSize*widthRatio)    
    master.customFontStage.configure(size=fontSize)
    
    # scales the text wrap in stage presentation    
    wrapLength = math.floor( IPTClock.wrapLength * widthRatio )
    IPTClock.presentationTextLabel.configure(wraplength= wrapLength)

    
def ResizeObjectsOnEvent(event):
    # activates scaling functions when resizing window
    SponsImageResize() # I know but it works

    
def SponsImageResize():
    IPTSpons.updateFigSize() # calls class function
    
######## OLD image presentation using just tkinter###########
#    # checks if the image is larger then the window and rescales. Slow process
#    global master
#    # get screen width and height    
#    ws = master.winfo_width() # width of the screen
#    hs = master.winfo_height() # height of the screen
#    
#    #get size of image
#    hi = master.image.height()
#    wi = master.image.width()

#    if ( hi > hs): #check i height of image is bigger then the window
#        scalefactor = hs/hi
#        new_width_pixels = round(ws / scalefactor )
#        new_height_pixels = hs
#
#        # since 
#        if ( math.log(new_height_pixels,10) > 2 ):
#            nlog =  math.log(new_height_pixels,10)
#            new_height_pixels = round( new_height_pixels / (10**( nlog-1) ) )
#            new_hi = round( hi / (10**( nlog-1) ) )            
#        else:
#            new_hi = hi
#
#        # since the only input is integers we need to scale up before we can scale down to reach good size
#        master.newImage = master.image.zoom(new_height_pixels) # Memory problems apears for higher values into zoom
#        master.newImage = master.newImage.subsample(new_hi) # and subsample back to desired size            
#        master.sponsLabel.configure(image = master.newImage)
    

def SponsImageFullscreen(a,b,c):
    IPTSpons.updateFigSize() # calls class update function
    
######## OLD image presentation using just tkinter###########
 #   global master
 #   ws = master.winfo_screenwidth() # width of the screen
 #   hs = master.winfo_screenheight() # height of the screen
 #   #get size of image
 #   hi = master.image.height()
 #   wi = master.image.width()
 #   if ( hi > hs): #check i height of image is bigger then the window
 #       scalefactor = hs/hi
 #       new_width_pixels = round(ws / scalefactor )
 #       new_height_pixels = hs
 #       
 #       # since 
 #       if ( math.log(new_height_pixels,10) > 2 ):
 #           nlog =  math.log(new_height_pixels,10)
 #           new_height_pixels = round( new_height_pixels / (10**( nlog-1) ) )
 #           new_hi = round( hi / (10**( nlog-1) ) )
 #           print('small')
 #       else:
 #           new_hi = hi
 #           # since the only input is integers we need to scale up before we can scale down to reach good size
 #       master.newImage = master.image.zoom(new_height_pixels) # Memory problems apears for higher values into zoom            
 #       master.newImage = master.newImage.subsample(new_hi) # and subsample back to desired size
 #   else:
 #       master.newImage = master.image
 #   master.sponsLabel.configure(image = master.newImage)
    
    
    
# about this application
def AboutPopup():
    # creates a popup window showing basic info and copywright
    top_about = tk.Toplevel()
    top_about.title("About IPTClock")

    about_logo=tk.Label(top_about, image=logo_image)
    about_logo.pack(side='left')

    about_message = "IPTClock is a countdown clock written for use in the International Physicist's Tournament. The program is written using Python 3 with Tkinter and matplotlib.\n\n Copyright (c) 2016-2017 by Albin Jonasson Svärdsby  \n Joel Magnusson"
    about_msg = tk.Message(top_about, text=about_message)
    about_msg.pack(side='right')

    about_exit_button = tk.Button(top_about, text="Dismiss", command=top_about.destroy)
    about_exit_button.pack(side='bottom')

###################
# GUI Definitions #
###################
master = tk.Tk()  # define master tk object

# fix icon on window
if usingWindows:
    pass
#    master.iconbitmap(default='./Images/Ico/newIPTlogo_without_text.ico') #'./Images/Ico/newIPTlogo_without_text.ico')

elif usingLinuxMasterRace:
    img = tk.PhotoImage(file='./Images/Ico/IPTlogo_color.png') #newIPTlogo_without_text.png')
    master.tk.call('wm', 'iconphoto', master._w, img)

elif usingMac:
    pass
else:
    pass

# change window title
master.wm_title("IPTClock")


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

######################################################

############################
# Define custom fonts and  #
# sizes for different text #
# objects                  #
############################

master.customFontButtons = tkFont.Font(family='Courier New', size=7)
master.customFontCompetitors = tkFont.Font(family='Courier New', size=12)
master.customFontDigitalClock = tkFont.Font(family='Courier New', size=30)
master.customFontStage = tkFont.Font(family='Courier New', size=16)

# save the original for use in scaling
master.customFontButtons_orig = master.customFontButtons.cget('size')
master.customFontCompetitors_orig = master.customFontCompetitors.cget('size')
master.customFontDigitalClock_orig = master.customFontDigitalClock.cget('size')
master.customFontStage_orig = master.customFontStage.cget('size')



# functions for changing font size
def IncreaseFontSize(event):
    # Funny wraparound might create strange things...
    fontSize = master.customFontCompetitors.cget('size')
    fontSize = fontSize + 1    
    master.customFontCompetitors.configure(size=fontSize)

    fontSize = master.customFontButtons.cget('size')
    fontSize = fontSize + 1    
    master.customFontButtons.configure(size=fontSize)

    fontSize = master.customFontDigitalClock.cget('size')
    fontSize = fontSize + 1    
    master.customFontDigitalClock.configure(size=fontSize)

    fontSize = master.customFontStage.cget('size')
    fontSize = fontSize + 1    
    master.customFontStage.configure(size=fontSize)

    
def DecreaseFontSize(event):
    fontSize = master.customFontCompetitors.cget('size')
    fontSize = fontSize - 1    
    master.customFontCompetitors.configure(size=fontSize)

    fontSize = master.customFontButtons.cget('size')
    fontSize = fontSize - 1    
    master.customFontButtons.configure(size=fontSize)

    fontSize = master.customFontDigitalClock.cget('size')
    fontSize = fontSize - 1    
    master.customFontDigitalClock.configure(size=fontSize)

    fontSize = master.customFontStage.cget('size')
    fontSize = fontSize - 1    
    master.customFontStage.configure(size=fontSize)



#################
# Sponsor Image #
#################

IPTSpons = SponsImage(master) # takes tk handle

### OLD image presentation using just tkinter###########
#master.image = tk.PhotoImage(file=leftSponsImagePath)
#master.sponsLabel = tk.Label(master, image=master.image)
#master.sponsLabel.grid(row=0, column=0, columnspan=1, rowspan=14, sticky='N')
#####################################################


####################
# Competitor Names #
####################
# Reporter
reporterLabel = tk.Label(master, text="Reporter:", font= master.customFontCompetitors)
reporterLabel.grid(row=11, column=2)
reporterLabel.configure(background=defaultBackgroundColor)
reporterNameLabel = tk.Label(master, text='Arnold Schwarzenegger', font= master.customFontCompetitors )
#reporterNameLabel = tk.Label(master, text='Starlight Glimmer', font=('Courier New', 16))
reporterNameLabel.grid(row=11, column=3, sticky=tk.W)

# Opponent
opponentLabel = tk.Label(master, text="Opponent:",font= master.customFontCompetitors)
opponentLabel.grid(row=12, column=2)
opponentLabel.configure(background=defaultBackgroundColor)
opponentNameLabel = tk.Label(master, text='Dwayne "The Rock" Johnson', font= master.customFontCompetitors)
#opponentNameLabel = tk.Label(master, text='Princess Twilight Sparkle', font=master.customFontCompetitors)
opponentNameLabel.grid(row=12, column=3, sticky=tk.W )

# Reviewer
reviewerLabel = tk.Label(master, text="Reviewer:", font=master.customFontCompetitors)
reviewerLabel.grid(row=13, column=2)
reviewerLabel.configure(background=defaultBackgroundColor)
reviewerNameLabel = tk.Label(master, text='Chuck Norris', font=master.customFontCompetitors)
#reviewerNameLabel = tk.Label(master, text='Shining Armor', font=master.customFontCompetitors)
reviewerNameLabel.grid(row=13, column=3, sticky=tk.W)

####################
# Initialize Clock #
####################
IPTClock = Clock(master) # takes tkHandle, 

# fix some font setup.
IPTClock.presentationTextLabel.configure(font = master.customFontStage) # updates the font and size of using defined font
IPTClock.countdownText.configure(font = master.customFontStage)



###################
# Control Buttons #
###################
# Start Button
startButton = tk.Button(master=master, text='Start', command=IPTClock.start, font= master.customFontButtons)
startButton.grid(row=4, column=7, sticky='WE')
startButton.configure(background=defaultBackgroundColor)

# Pause Button
pauseButton = tk.Button(master=master, text='Pause', command=IPTClock.pause, font= master.customFontButtons)
pauseButton.grid(row=5, column=7, sticky='WE')
pauseButton.configure(background=defaultBackgroundColor)

# Reset button
resetButton = tk.Button(master=master, text='Reset', command=IPTClock.reset, font= master.customFontButtons)
resetButton.grid(row=11, column=7, sticky='WE')
resetButton.configure(background=defaultBackgroundColor)

# Quit button
quitButton = tk.Button(master=master, text='Quit', command=_quit, font= master.customFontButtons)
quitButton.grid(row=13, column=7, sticky='WE')
quitButton.configure(background=defaultBackgroundColor)

# Fullscreen
fullscreenButton = tk.Button(master=master, text='Fullscreen', command=toogleFullscreenButton, font= master.customFontButtons)
fullscreenButton.grid(row=7, column=7, sticky='WE')
fullscreenButton.configure(background=defaultBackgroundColor)

# Edit Reporter
editReporterButton = tk.Button(master=master, text='Edit', command=EditReporter, font= master.customFontButtons)
editReporterButton.grid(row=11, column=5)
editReporterButton.configure(background=defaultBackgroundColor)

# Edit Opponent
editOpponentButton = tk.Button(master=master, text='Edit', command=EditOpponent, font= master.customFontButtons)
editOpponentButton.grid(row=12, column=5)
editOpponentButton.configure(background=defaultBackgroundColor)

# Edit Reviewer
editReviewerButton = tk.Button(master=master, text='Edit', command=EditReviewer, font= master.customFontButtons)
editReviewerButton.grid(row=13, column=5)
editReviewerButton.configure(background=defaultBackgroundColor)

# Previous Stage
previousStageButton = tk.Button(master=master, text='<<', command=IPTClock.previous_stage, font= master.customFontButtons)
previousStageButton.grid(row=8, column=7, sticky='WE')

# Next Stage
nextStageButton = tk.Button(master=master, text='>>', command=IPTClock.next_stage, font= master.customFontButtons)
nextStageButton.grid(row=9, column=7, sticky='WE')

# timeout
timeoutButton = tk.Button(master=master, text='Timeout', command=lambda clockHandle = IPTClock: Timeout(clockHandle) , font= master.customFontButtons) 
timeoutButton.grid(row=10,column=7,sticky='WE')


#####################
# layout lines
####################
horizontalLine = tk.Label(master, text='-', background='darkgray', height=1, font=('Courier New', 1), borderwidth=0)
horizontalLine.grid(row=10, column=2, columnspan=4, sticky='WE')

verticalLineRight = tk.Label(master, text='-', background='darkgray', height=1, font=('Courier New', 1), borderwidth=0)
verticalLineRight.grid(row=0, column=6, columnspan=1, rowspan=14, sticky='NS')

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

## help menu ##
logo_image = tk.PhotoImage(file= './Images/IPTlogos/IPTlogo_Color.gif') #'./Images/IPTlogos/newIPTlogo_without_text.gif') # needed outside aboutPopup to avoid garbage collect

helpmenu = tk.Menu(menubar, tearoff=0) # create helpmenu
helpmenu.add_command(label="About", command= AboutPopup )

menubar.add_cascade(label="Help", menu=helpmenu) # add helpmenu
master.config(menu=menubar) # set the final menu


#######################################
# change column behaviour for scaling #
#######################################
master.rowconfigure(0, weight=1)
#master.rowconfigure(1, weight=1)
#master.rowconfigure(2, weight=1)#, minsize = 200)
master.rowconfigure(3, weight=2)
master.rowconfigure(9, minsize=125)

master.columnconfigure(0, weight=1, minsize = 100) # minsize to ensure that sponsor logo is visible
#master.columnconfigure(1, weight=1)
master.columnconfigure(3, weight=1)
#master.columnconfigure(7, minsize=240)
#master.columnconfigure(7, weight=1)


#######################
# Initial window size #
#######################

# fix initial window size and position
w = 640 #900 # width for the Tk root [pixels]
h = 480 #700 # height for the Tk root
# get screen width and height
ws = master.winfo_screenwidth() # width of the screen [pixels]
hs = master.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

master.geometry('%dx%d+%d+%d' % (w, h, x, y))

####################
# Window rescaling #
####################

# binds resize of master window and execute rescale of spons image
master.fullscreenSwitch = tk.BooleanVar() # variable to trace
master.fullscreenSwitch.set(False) # initial value

master.fullscreenSwitch.trace('w', SponsImageFullscreen) # watch the variable master.fullscreenSwitch, when i changes on switching to fullscreen it will execute command SponsImageFullscreen

# if close using window manager    
master.protocol("WM_DELETE_WINDOW", on_closing)  # necessary to cleanly exit the program when using the windows manager

# resize by dragging window
master.bind('<Configure>', ResizeObjectsOnEvent )


#####################
# Keyboard bindings #
#####################



# bindings for fullscreen
master.fullscreen = False
master.attributes('-fullscreen', False)

if usingLinuxMasterRace or usingMac:
    master.bind("<F11>", toogleFullscreenLinux)
    master.bind("<Escape>", endFullscreenLinux)
else:
    master.bind("<F11>", toogleFullscreen)    
    master.bind("<Escape>", endFullscreen)

# bindings for changing stage
def KeyNextStage(event):
    IPTClock.next_stage()    
master.bind("<Control-Right>", KeyNextStage )

def KeyPreviousStage(event):
    IPTClock.previous_stage()    
master.bind("<Control-Left>", KeyPreviousStage )


# change font size    
master.bind("<Control-plus>", IncreaseFontSize)
master.bind("<Control-KP_Add>", IncreaseFontSize)

master.bind("<Control-minus>", DecreaseFontSize)
master.bind("<Control-KP_Subtract>", DecreaseFontSize)    
#######################
# Final loop commands #
#######################

IPTClock.update()  # update the countdown during GUI loop

# start the GUI loop
master.mainloop()
