
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
#    sys.exit(0)
    usePython3 = False
else:    
    import _thread # in order to utilize threads # the threading that is used is written for python 3
    usePython3 = True

# import tkinter
if usePython3: 
    import tkinter as tk
    from tkinter import messagebox # used for popups
    from tkinter import simpledialog
    import tkinter.font as tkFont # used for custom font settings
else:
    #python2 compatibility
    import Tkinter as tk
    import tkMessageBox as messagebox# used for popups
    import tkSimpleDialog as simpledialog
    import tkFont # used for custom font settings

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
def TimeoutMaster(event):
    Timeout(master.IPTClock)

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
        if usingWindows:
            master.destroy()
            #exit()
        sys.exit(0)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        if usingWindows:
            master.destroy()
            #exit()
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
    FontResize(int(screenWidth))
    SponsImageResize()
    

def endFullscreenLinux(tmp):
    endFullscreen() # there's some difference between os and input using keyes
    

def endFullscreen():
    global master, fullscreenButton
    if master.fullscreen:
        master.fullscreen = False
        master.attributes("-fullscreen", False)
        fullscreenButton.configure(text="Fullscreen")
        master.focus_set()
		
    #fullscreenButton.configure(text="Fullscreen")
        master.fullscreenSwitch.set(False) # traced variable
        screenWidth = 640
    FontResize(screenWidth)
    SponsImageResize() # needed since it might skip resizing back elsewise


def EditReporterEvent(event):
    EditReporter()

def EditReporter():    
    master.reporterString = simpledialog.askstring('Edit Reporter', 'Reporter', initialvalue=master.reporterNameLabel.cget('text') )
    master.reporterNameLabel.configure(text=master.reporterString)

def EditOpponentEvent(event):
    EditOpponent()
    
def EditOpponent():
    master.opponentString = simpledialog.askstring('Edit Opponent', 'Opponent', initialvalue=master.opponentNameLabel.cget('text'))
    master.opponentNameLabel.configure(text=master.opponentString)

def EditReviewerEvent(event):
    EditReviewer()
    
def EditReviewer():
    master.reviewerString = simpledialog.askstring('Edit Reviewer', 'Reviewer', initialvalue=master.reviewerNameLabel.cget('text'))
    master.reviewerNameLabel.configure(text=master.reviewerString)


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
    fontSize = int( math.floor(fontSize*widthRatio) )
    master.customFontCompetitors.configure(size=fontSize)
    master.competitorFontSize.set(fontSize)
    
    fontSize = master.customFontButtons_orig
    fontSize = int( math.floor(fontSize*widthRatio) )
    #if (abs(fontSize) > 16):
    if fontSize < master.minButtonFontSize:
        fontSize = master.minButtonFontSize
    master.customFontButtons.configure(size=fontSize)
    master.buttonFontSize.set(fontSize)
    
    fontSize = master.customFontDigitalClock_orig
    fontSize = int( math.floor(fontSize*widthRatio) )
    master.customFontDigitalClock.configure(size=fontSize)
    master.digitalClockFontSize.set(fontSize)
    
    fontSize = master.customFontStage_orig
    fontSize = int( math.floor(fontSize*widthRatio) )
    
    # ensure stage fontsize is below imposed limit
    if( fontSize > master.maxStageFontSize):    
        master.customFontStage.configure(size=master.maxStageFontSize)
    else:
        master.customFontStage.configure(size=fontSize)
    master.stageFontSize.set(fontSize)
    
    
    # scales the text wrap in stage presentation    
    wrapLength = math.floor( master.IPTClock.wrapLength * widthRatio  )
    master.IPTClock.presentationTextLabel.configure(wraplength= wrapLength)
    
    
def ResizeObjectsOnEvent(event):
    # activates scaling functions when resizing window
    SponsImageResize() # I know but it works

# Removed since it counters manual changes.    
#    frameWidthPixels = master.winfo_width()
#    FontResize(frameWidthPixels)
    
    
def SponsImageResize():
    master.IPTSpons.updateFigSize() # calls class function
    
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
    master.IPTSpons.updateFigSize() # calls class update function
    
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


 # Set stage time
def SetStageStartTime(start_time):    
    master.IPTClock.set_stage_startTime(start_time)


# Popup for setting time of countdownclock
def SetTimePopUp(event):
    correctInput = False
    dialogString = tk.StringVar()
    dialogString.set("How much time has passed?")
    
    while not correctInput:
        initialTime = tk.IntVar()
        initialTime.set(0)
        timeInteger = simpledialog.askinteger("Set Time",dialogString.get(), initialvalue=initialTime.get())

        # check None in case termination with "windows cross"
        if timeInteger is None:            
            break
        else:            
            # check validity
            if timeInteger < 0 or abs(timeInteger) > master.IPTClock.stage.time():
                correctInput = False
                dialogString.set("Insert valid time range!")
            else:
                correctInput = True

    if correctInput:
        SetStageStartTime(timeInteger)


def IncreaseTime(event):
    timeStep = 5
    MoveTime( timeStep )

def DecreaseTime(event):
    timeStep = -5
    MoveTime( timeStep )

def MoveTime(timeMoved):
    time = master.IPTClock.timer.time()      
    # validity check
  #  if (time - timeMoved) < 0:
  #      timeMoved = 0
    master.IPTClock.timer.set_time(time - timeMoved) # to decrease we here add
    master.IPTClock.refresh()

    
# about this application
def AboutPopup():
    # creates a popup window showing basic info and copywright
    top_about = tk.Toplevel()
    top_about.title("About IPTClock")
    top_about.configure(bg = defaultBackgroundColour)

    about_frame = tk.Frame(top_about)
    about_frame.configure(bg = defaultBackgroundColour)
#    about_logo=tk.Label(top_about, image=logo_image)
    about_logo=tk.Label(about_frame, image=logo_image)
    about_logo.pack(side='left')
    about_logo.configure( bg = defaultBackgroundColour )

    about_message = "IPTClock is a countdown clock written for use in the International Physicist's Tournament. The program is written using Python 3 with Tkinter and matplotlib.\n\n Copyright (c) 2016-2017 by Albin Jonasson Svärdsby  \n Joel Magnusson"
#    about_msg = tk.Message(top_about, text=about_message)
    about_msg = tk.Message(about_frame, text=about_message)
    about_msg.pack(side='right')
    about_msg.configure(bg = defaultBackgroundColour, fg=textColour)

    about_frame.pack(side='top')
    about_exit_button = tk.Button(top_about, text="Dismiss", command=top_about.destroy)
    about_exit_button.pack(side='bottom')
    about_exit_button.configure(bg = defaultBackgroundColour, fg=textColour)

    centerTop(top_about)

def centerTop(toplevel):
    # centering the top widget
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    
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


# set the background colour, given from variable at start
master.configure(background=defaultBackgroundColour)


# Find default background colour and check in case we use it
defaultbgColour = master.cget('bg')  # find system window default colour
bgRGB = master.winfo_rgb(defaultbgColour)
bgRGB = (bgRGB[0]/(256**2), bgRGB[1]/(256**2), bgRGB[2]/(256**2))

if wedgeBackgroundColour is None:
    wedgeBackgroundColour = bgRGB

# boolean for fullscreen
master.fullscreen = False

######################################################

############################
# Define custom fonts and  #
# sizes for different text #
# objects                  #
############################

master.customFontButtons = tkFont.Font(family=defaultFont, size=7)
master.minButtonFontSize = 7 # min font size for buttons

master.customFontCompetitors = tkFont.Font(family=defaultFont, size=12)
master.customFontDigitalClock = tkFont.Font(family=defaultFont, size=32)

master.customFontStage = tkFont.Font(family=defaultFont, size=16)
master.maxStageFontSize = 57 # imposed limitation for font size

# variables to keep track of the font size value, if outside imposed limitations.
# need to be intvar for use in spinbox
master.buttonFontSize = tk.IntVar(master)
master.buttonFontSize.set( master.customFontButtons.cget('size') )

master.competitorFontSize = tk.IntVar(master)
master.competitorFontSize.set(master.customFontCompetitors.cget('size') )

master.stageFontSize = tk.IntVar(master)
master.stageFontSize.set(master.customFontStage.cget('size'))

master.digitalClockFontSize = tk.IntVar(master)
master.digitalClockFontSize.set(master.customFontDigitalClock.cget('size') )


# save the original for use in scaling
master.customFontButtons_orig = master.customFontButtons.cget('size')
master.customFontCompetitors_orig = master.customFontCompetitors.cget('size')
master.customFontDigitalClock_orig = master.customFontDigitalClock.cget('size')
master.customFontStage_orig = master.customFontStage.cget('size')
 


# functions for changing font size
def IncreaseFontSize(event):
    # Funny wraparound might create strange things...
    fontSize = master.customFontCompetitors.cget('size') # save as variable in master object.
    fontSize = fontSize + 1    
    master.customFontCompetitors.configure(size=fontSize)

    fontSize = master.buttonFontSize.get()
    fontSize = fontSize + 1

    # ensure the buttons doesn't get to small
    if fontSize < master.minButtonFontSize:
        master.customFontButtons.configure(size=master.minButtonFontSize)
    else:
        master.customFontButtons.configure(size=fontSize)
    master.buttonFontSize.set(fontSize)

    fontSize = master.customFontDigitalClock.cget('size')
    fontSize = fontSize + 2    
    master.customFontDigitalClock.configure(size=fontSize)

    
    fontSize = master.customFontStage.cget('size')
    fontSize = fontSize + 1
    
    # ensure stage fontsize is below imposed limit
    if( fontSize > master.maxStageFontSize):    
        master.customFontStage.configure(size=master.maxStageFontSize)
    else:
        master.customFontStage.configure(size=fontSize)
    master.stageFontSize.set(fontSize)

    
def DecreaseFontSize(event):
    fontSize = master.customFontCompetitors.cget('size')
    fontSize = fontSize - 1    
    master.customFontCompetitors.configure(size=fontSize)

    fontSize = master.buttonFontSize.get()
    fontSize = fontSize - 1

    # ensure the buttons doesn't get to small
    if fontSize < master.minButtonFontSize:
        master.customFontButtons.configure(size=master.minButtonFontSize)
    else:
        master.customFontButtons.configure(size=fontSize)
    master.buttonFontSize.set(fontSize)
        
    fontSize = master.customFontDigitalClock.cget('size')
    fontSize = fontSize - 2    
    master.customFontDigitalClock.configure(size=fontSize)

    fontSize = master.customFontStage.cget('size')
    fontSize = fontSize - 1

    # ensure stage fontsize is below imposed limit
    if( fontSize > master.maxStageFontSize):    
        master.customFontStage.configure(size=master.maxStageFontSize)
    else:
        master.customFontStage.configure(size=fontSize)
    master.stageFontSize.set(fontSize)
    

def SetToDefaultFontSize(event):
    # Set default values for font sizes
    master.customFontButtons.configure(size= master.customFontButtons_orig)
    master.customFontCompetitors.configure(size= master.customFontCompetitors_orig)
    master.customFontDigitalClock.configure(size= master.customFontDigitalClock_orig)
    master.customFontStage.configure(size= master.customFontStage_orig)

    # call window scaling
    if (master.fullscreen):
         screenWidth = master.winfo_screenwidth() 
    else:
        screenWidth = 640
    FontResize(int(screenWidth))


###########################
# Configure menu
##########################
def StartConfigureEvent(event):
    StartConfigure()

def StartConfigure():
    # created EditFrame class to create
    # a top frame for configuring fontsizes
    master.EditFrame = EditFrame(master)

    # make sure the same keybindings work even if the edit window is up.
    master.EditFrameBindings = KeyBindingClass(master.EditFrame.top)
    
#################
# Sponsor Image #
#################

# IPTSpons = SponsImage(master) # uses matplotlib to render image
master.IPTSpons = SponsImagePillow(master) # uses PIL and tkinter to render image (fastest)

### OLD image presentation using just tkinter###########
#master.image = tk.PhotoImage(file=leftSponsImagePath)
#master.sponsLabel = tk.Label(master, image=master.image)
#master.sponsLabel.grid(row=0, column=0, columnspan=1, rowspan=14, sticky='N')
#####################################################



####################
# Competitor Names #
####################
## Reporter ##
master.reporterLabel = tk.Label(master, text="Reporter:", font= master.customFontCompetitors)
master.reporterLabel.grid(row=11, column=2)
master.reporterLabel.configure(background=defaultBackgroundColour, fg= textColour)
master.reporterLabel.bind("<Button-1>",EditReporterEvent)
master.reporterNameLabel = tk.Label(master, text='Arnold Schwarzenegger', font= master.customFontCompetitors )
#reporterNameLabel = tk.Label(master, text='Starlight Glimmer', font=('Courier New', 16))
master.reporterNameLabel.grid(row=11, column=3, sticky=tk.W)
master.reporterNameLabel.configure(background=defaultBackgroundColour, fg= textColour)
master.reporterNameLabel.bind("<Button-1>",EditReporterEvent)


## Opponent ##
master.opponentLabel = tk.Label(master, text="Opponent:",font= master.customFontCompetitors)
master.opponentLabel.grid(row=12, column=2)
master.opponentLabel.configure(background=defaultBackgroundColour, fg= textColour)
master.opponentLabel.bind("<Button-1>",EditOpponentEvent)

master.opponentNameLabel = tk.Label(master, text='Dwayne "The Rock" Johnson', font= master.customFontCompetitors)
#opponentNameLabel = tk.Label(master, text='Princess Twilight Sparkle', font=master.customFontCompetitors)
master.opponentNameLabel.grid(row=12, column=3, sticky=tk.W )
master.opponentNameLabel.configure(background=defaultBackgroundColour, fg= textColour)
master.opponentNameLabel.bind("<Button-1>",EditOpponentEvent)


## Reviewer ##
master.reviewerLabel = tk.Label(master, text="Reviewer:", font=master.customFontCompetitors)
master.reviewerLabel.grid(row=13, column=2)
master.reviewerLabel.configure(background=defaultBackgroundColour, fg= textColour)
master.reviewerLabel.bind("<Button-1>",EditReviewerEvent)

master.reviewerNameLabel = tk.Label(master, text='Chuck Norris', font=master.customFontCompetitors)
#reviewerNameLabel = tk.Label(master, text='Shining Armor', font=master.customFontCompetitors)
master.reviewerNameLabel.grid(row=13, column=3, sticky=tk.W)
master.reviewerNameLabel.configure(background=defaultBackgroundColour, fg= textColour)
master.reviewerNameLabel.bind("<Button-1>",EditReviewerEvent)

####################
# Initialize Clock #
####################
master.IPTClock = Clock(master) # takes tkHandle, 

# fix some font setup.
master.IPTClock.presentationTextLabel.configure(font = master.customFontStage) # updates the font and size of using defined font
master.IPTClock.countdownText.configure(font = master.customFontDigitalClock)
master.IPTClock.countdownText.bind("<Button-1>", SetTimePopUp)


###################
# Control Buttons #
###################

# Create frame for top buttons

controlButton_frame = tk.Frame(master)
controlButton_frame.grid(row=3, column=7, rowspan=7, sticky="WES", pady=20)

startButton = tk.Button(master=controlButton_frame, text='Start', command=master.IPTClock.start, font= master.customFontButtons)
startButton.configure(background=defaultBackgroundColour, fg= textColour)
startButton.grid(row=0, sticky="WE")

# Pause Button
pauseButton = tk.Button(master=controlButton_frame, text='Pause', command=master.IPTClock.pause, font= master.customFontButtons)
pauseButton.configure(background=defaultBackgroundColour, fg= textColour)
pauseButton.grid(row=1, sticky="WE")

# Fullscreen
fullscreenButton = tk.Button(master=controlButton_frame, text='Fullscreen', command=toogleFullscreenButton, font= master.customFontButtons)
fullscreenButton.configure(background=defaultBackgroundColour, fg= textColour)
fullscreenButton.grid(row=2, sticky="WE")

# Previous Stage
previousStageButton = tk.Button(master=controlButton_frame, text='<<', command=master.IPTClock.previous_stage, font= master.customFontButtons)
previousStageButton.configure(background=defaultBackgroundColour, fg= textColour)
previousStageButton.grid(row=3, sticky="WE")

# Next Stage
nextStageButton = tk.Button(master=controlButton_frame, text='>>', command=master.IPTClock.next_stage, font= master.customFontButtons)
nextStageButton.configure(background=defaultBackgroundColour, fg= textColour)
nextStageButton.grid(row=4, sticky="WE")

# timeout
def HandleReturn():
    return master.IPTClock, master

# Timeout button
timeoutButton = tk.Button(master=master, text='Timeout', command=lambda clockHandle = master.IPTClock: Timeout(clockHandle) , font= master.customFontButtons)
timeoutButton.configure(background=defaultBackgroundColour, fg= textColour)
timeoutButton.grid(row=10,column=7,sticky='WE')


# Reset button
resetButton = tk.Button(master=master, text='Reset', command=master.IPTClock.reset, font= master.customFontButtons)
resetButton.configure(background=defaultBackgroundColour, fg= textColour)
resetButton.grid(row=11, column=7, sticky='WEN')

# Quit button
quitButton = tk.Button(master=master, text='Quit', command=_quit, font= master.customFontButtons)
quitButton.configure(background=defaultBackgroundColour, fg= textColour)
quitButton.grid(row=13, column=7, sticky='WE')


# Removed Edit buttons
"""
# Edit Reporter
editReporterButton = tk.Button(master=master, text='Edit', command=EditReporter, font= master.customFontButtons)
editReporterButton.configure(background=defaultBackgroundColour, fg= textColour)
editReporterButton.grid(row=11, column=5)

# Edit Opponent
editOpponentButton = tk.Button(master=master, text='Edit', command=EditOpponent, font= master.customFontButtons)
editOpponentButton.configure(background=defaultBackgroundColour, fg= textColour)
editOpponentButton.grid(row=12, column=5)

# Edit Reviewer
editReviewerButton = tk.Button(master=master, text='Edit', command=EditReviewer, font= master.customFontButtons)
editReviewerButton.configure(background=defaultBackgroundColour, fg= textColour)
editReviewerButton.grid(row=13, column=5)
"""


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

## add file menu ##
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_separator()

filemenu.add_command(label="Exit", command=_quit)
menubar.add_cascade(label="File", menu=filemenu)

# drop down menu to chose stage
stagemenu = tk.Menu(menubar, tearoff=0)
for i, stage in enumerate(master.IPTClock.stage.get_stages()):
    stagemenu.add_command(label=str(i) + ": " + stage[0],
                          command=lambda stage_number=i: master.IPTClock.set_stage(stage_number))

menubar.add_cascade(label="Stage", menu=stagemenu)

## edit menu ##
editmenu = tk.Menu(menubar,tearoff = 0) # creates edit menu
editmenu.add_command(label="Configure", command = StartConfigure)
menubar.add_cascade(label="Edit", menu = editmenu)


## help menu ##
logo_image = tk.PhotoImage(file= './Images/IPTlogos/IPTlogo_color_small.gif') #'./Images/IPTlogos/newIPTlogo_without_text.gif') # needed outside aboutPopup to avoid garbage collect

helpmenu = tk.Menu(menubar, tearoff=0) # create helpmenu
helpmenu.add_command(label="About",  command= AboutPopup )

menubar.add_cascade(label="Help", menu=helpmenu) # add helpmenu
master.config(menu=menubar) # set the final menu


#######################################
# change column behaviour for scaling #
#######################################
#master.rowconfigure(0, weight=1)
#master.rowconfigure(1, weight=1)
#master.rowconfigure(2, weight=1)#, minsize = 200)
master.rowconfigure(3, weight=2)

master.rowconfigure(9, minsize=125)

#master.sponsWidth = 150
master.sponsWidth = tk.IntVar()
master.sponsWidth.set(150)
master.columnconfigure(0, weight=2, minsize = master.sponsWidth.get()) # minsize to ensure that sponsor logo is visible
#master.columnconfigure(0, weight=1, minsize = master.sponsWidth) # minsize to ensure that sponsor logo is visible
#master.columnconfigure(1, weight=1)
####master.columnconfigure(3, weight=1)
master.clockWidth = 250
master.columnconfigure(3, weight=1, minsize= master.clockWidth )
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


# Methods for manually change size of sponsor column
def IncreaseSponsWidth(event):
#    master.sponsWidth = master.sponsWidth + 1
    master.sponsWidth.set( master.sponsWidth.get() +1 )
    master.columnconfigure(0, weight=2, minsize = master.sponsWidth.get() )
    SponsImageResize()
    
def DecreaseSponsWidth(event):
#    master.sponsWidth = master.sponsWidth -1
    master.sponsWidth.set( master.sponsWidth.get() - 1)
    master.columnconfigure(0, weight=2, minsize = master.sponsWidth.get() )    
    SponsImageResize()
    
#####################
# Keyboard bindings #
#####################

# bindings for fullscreen
master.fullscreen = False
master.attributes('-fullscreen', False)



class KeyBindingClass():
    # for dealing with key bindings
    
    def __init__(self,tkHandle):
        self.tk_handle = tkHandle        

        if usingLinuxMasterRace or usingMac:
            self.tk_handle.bind("<F11>", toogleFullscreenLinux)
            self.tk_handle.bind("<Escape>", endFullscreenLinux)
        else:
            self.tk_handle.bind("<F11>", toogleFullscreenLinux)
            self.tk_handle.bind("<Escape>", endFullscreenLinux)
            #    master.bind("<F11>", toogleFullscreen)    
            #    master.bind("<Escape>", endFullscreen)

        if usingMac:
            self.tk_handle.bind("<Command-Right>", self.KeyNextStage )
        else:
            self.tk_handle.bind("<Control-Right>", self.KeyNextStage )

        if usingMac:
            self.tk_handle.bind("<Command-Left>", self.KeyPreviousStage )
        else:
            self.tk_handle.bind("<Control-Left>", self.KeyPreviousStage )

        if usingLinuxMasterRace:
            self.tk_handle.bind("<Control-0x003d>", IncreaseFontSize) # for =, doesn't work on windows.

        if usingLinuxMasterRace or usingWindows:
            self.tk_handle.bind("<Control-r>", self.keyboardReset)
            self.tk_handle.bind("<Control-KP_Enter>", self.keyboardStartPaus)
            self.tk_handle.bind("<Control-Return>", self.keyboardStartPaus)
            self.tk_handle.bind("<Control-k>", IncreaseSponsWidth)
            self.tk_handle.bind("<Control-j>", DecreaseSponsWidth)
	
            ## change font size ##
            # increase
            self.tk_handle.bind("<Control-plus>", IncreaseFontSize)
            self.tk_handle.bind("<Control-KP_Add>", IncreaseFontSize) #keypad +            

            # decrease
            self.tk_handle.bind("<Control-minus>", DecreaseFontSize)
            self.tk_handle.bind("<Control-KP_Subtract>", DecreaseFontSize) #keypad -

            # default size
            self.tk_handle.bind("<Control-KP_0>", SetToDefaultFontSize)
            self.tk_handle.bind("<Control-0>", SetToDefaultFontSize) #keypad 0

            # update start time
            self.tk_handle.bind("<Control-u>", SetTimePopUp )

            # increase and decrease timer
            self.tk_handle.bind("<Control-m>", IncreaseTime)
            self.tk_handle.bind("<Control-n>", DecreaseTime)

            # fullscreen
            self.tk_handle.bind("<Control-f>", toogleFullscreenLinux )

            # timeout
            self.tk_handle.bind("<Control-t>", TimeoutMaster )

            # open config menu
            self.tk_handle.bind("<Control-c>", StartConfigureEvent )

            
        else:
            self.tk_handle.bind("<Command-r>", self.keyboardReset)
            self.tk_handle.bind("<Command-KP_Enter>", self.keyboardStartPaus)
            self.tk_handle.bind("<Command-Return>", self.keyboardStartPaus)
            self.tk_handle.bind("<Command-k>", IncreaseSponsWidth)
            self.tk_handle.bind("<Command-j>", DecreaseSponsWidth)
	
	    ## change font size ##
            # increase
            self.tk_handle.bind("<Command-plus>", IncreaseFontSize)
            self.tk_handle.bind("<Command-KP_Add>", IncreaseFontSize) #keypad +
   #         self.tk_handle.bind("<Command-0x003d>", IncreaseFontSize)
    
            # decrease
            self.tk_handle.bind("<Command-minus>", DecreaseFontSize)
            self.tk_handle.bind("<Command-KP_Subtract>", DecreaseFontSize) #keypad -

            # default size
            self.tk_handle.bind("<Command-KP_0>", SetToDefaultFontSize)
            self.tk_handle.bind("<Command-0>", SetToDefaultFontSize) #keypad 0
    
            # update start time
            self.tk_handle.bind("<Command-u>", SetTimePopUp  )
        
            # increase and decrease timer
            self.tk_handle.bind("<Command-m>", IncreaseTime)
            self.tk_handle.bind("<Command-n>", DecreaseTime)
            
            # fullscreen
            self.tk_handle.bind("<Command-f>", toogleFullscreenLinux )

            # timeout
            self.tk_handle.bind("<Command-t>", TimeoutMaster )

            # open config menu
            self.tk_handle.bind("<Command-c>", StartConfigureEvent )

        
            # bindings for changing stage
    def KeyNextStage(self,event):
        master.IPTClock.next_stage()
    
            
    def KeyPreviousStage(self,event):
        master.IPTClock.previous_stage()        
    

            ## bindings for start and stop 
    def keyboardStartPaus(self,event):
        if master.IPTClock.timer.isTicking():
            master.IPTClock.pause()
        else:
            master.IPTClock.start()
    
    def keyboardReset(self,event):
        master.IPTClock.reset()
        master.IPTClock.start()    
    

# activate keybindings for master    
master.KeyBindings = KeyBindingClass(master)
        


#######################
# Final loop commands #
#######################

master.IPTClock.update()  # update the countdown during GUI loop


# ugly exception capture
while True:
    try:

        # start the GUI loop
        master.mainloop()
        break
    except UnicodeDecodeError:
        pass
