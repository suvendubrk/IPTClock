# check tkversion

# Import packages
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import _thread #in order to utilize threads
    
#import tkfont #to change font 

#Check for matplotlib and import ELSE DOESN'T DRAW GRAPHICS
modules = set(["matplotlib"])
for module in modules:
    try:
        __import__(module)
        # imports the matplotlib and set variable installedMatplotlib
        installedMatplotlib = True
        
        import matplotlib as mplotlib
        mplotlib.use('TkAgg')

        import matplotlib.patches as mpatches
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

    except ImportError:
        installedMatplotlib = False
        print('No Matplotlib installed!!! \n Functionality crippled! ')

######################################################
import matplotlib as mplotlib
mplotlib.use('TkAgg')	
installedMatplotlib = True
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#########################################################
# check if we use audio or not (.wave format)
try:
    import pyaudio
    installedPyaudio = True
except ImportError:
    installedPyaudio = False

if (installedPyaudio):
    import wave

        
# for converting and accepting more fileformats for photos, NOT IMPLEMENTED
#from PIL import Image, ImageTk


####### global variables of use, to change each IPT year ##################

presentationText = "IPT 2017 Göteborg" # should be string, text that shows at start

## To be introduced...:
# defaultFont = # string deciding the standard font
# defaultFontSize =  # integer, fontsize of text
defaultBackgroundColor = None #'blue'    # String, following tkinter naming. color used for background, buttons and labels etc. NOT color behind wedge, use "None" without "" to get system default
wedgeBackgroundColor = None # '#13235b' #String, following matplotlib naming.  color of the wedge background (for example to adhere to present year's color scheme
wedgeColor = '#ffe000' # String, following matplotlib naming. color of the wedge (for example to adhere to present year's color scheme
#leftSponsImagePath = './Albin-300x286.gif'
leftSponsImagePath = './ponyAndDuck.gif'

pathToSoundFile = ''#'allahu.wav' #'SaleelSawarimNasheed.wav' # If left empty nothing happens


 
# function updating the time
def update_countdown():

    global countdownTime #variable containing seconds left
    global countdownState
   
    # Every time this function is called, 
    # decrease countdownTime with one second
    
        
    if (countdownTime <= 0 ):
        countdownState = False

    if (countdownState):
        countdownTime -= 1
        #run the functions updating the graphical representation
        update_countdownText()
        update_angle()
        
        # check for countdown time for activating "low health mode"
        if ( countdownTime == 55):
            _thread.start_new_thread(PlayASoundFile, (pathToSoundFile,) )

        
    # Call the update_countdown() function after 1 second
    master.after(1000, update_countdown) #wait 1000 [ms]


# function updating the presented digital countdown
def update_countdownText():
    if (countdownState):
        global countdownTime #variable containing seconds left
             
          
        # create string for countdownTimer
        timerSeconds = countdownTime % 60
        timerMinutes = countdownTime // 60
        
        timeString = pattern.format(timerMinutes, timerSeconds)
        # Update the countdownText Label with the updated time
        countdownText.configure(text=timeString)
        
       

# Function updating and drawing the "pie wedge" for the countdown
def update_angle():
     if (countdownState):
         global countdownTime, countdownStartTime

         #         if ( (countdownTime%2) > 0 ): # in case draw is taxing
         
         #angle starts at 90 then negative direction clockwise
         angle = 90 - 360*( (countdownStartTime-countdownTime) /countdownStartTime )
         currentAngle = angle
         DrawWedgeOnCanvas(currentAngle )



##### the commands for the buttons #####
    
# To start the countdown
def StartCountdown():
    global countdownState
#    ResetCountdown
    countdownState = True

# To pause the countdown
def PausCountdown():
    global countdownState
    countdownState = False

# To reset the countdown to startTime
def ResetCountdown():
    global countdownTime, countdownStartTime
    countdownTime = countdownStartTime 

    # create string for countdownTimer
    timerSeconds = countdownTime % 60
    timerMinutes = countdownTime // 60
        
    timeString = pattern.format(timerMinutes, timerSeconds)
    # Update the countdownText Label with the updated time
    countdownText.configure(text=timeString)

    #update the wedge on canvas
    currentAngle=90
    DrawWedgeOnCanvas(currentAngle)


# emphesise quit()
def _quit():
    master.quit()     # stops mainloop
    master.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


###############################
# canvas for drawing wedge
##############################
def DrawWedgeOnCanvas(currentAngle):
    if (installedMatplotlib): # doesn't draw the wedge in case no matplotlib dependencies
        global  wedgeBackgroundColor, wedgeColor
        
        startPos =[0,0]
        startAngle = 90
        R = 0.9
        #    currentAngle = -170 # angle in [90,-270]
        
        fig = plt.figure(figsize=(16,16), facecolor=wedgeBackgroundColor) # figsize is used to make sure the countdown wedge is large enough. If you find it to small, increase the figsize.
        ax = fig.add_subplot(111)

        wedge=mpatches.Wedge(startPos, R, currentAngle, startAngle, facecolor=wedgeColor)

        
        #adds circle at along perimeter
        perimeterCircle=mpatches.Circle(startPos, R, fill=False)
        ax.add_patch(perimeterCircle)
    
        ax.add_patch(wedge) # add wedge
        ax.set_xlim(-1,1)
        ax.set_ylim(-1,1)


        #remove axis and ticks
        plt.tick_params(
            axis='both',       # changes apply to both axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off', # labels along the bottom edge are off
            labelleft='off')   # labels to the left

        plt.axis('equal')     # equal axis 
        plt.axis('off')       # removes axis from figure


        canvas2 = FigureCanvasTkAgg(fig, master=master)
        canvas2.show()
        canvas2.get_tk_widget().grid(row=0, column =2, columnspan=3, rowspan= 3, sticky=tk.N)


######### For playing sound ##########
def PlayASoundFile(pathToSoundFile):
    CHUNK = 64#1024
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


################# For displaying gif moving ####################




    

#### DEFINITION OF STAGES ###############
            
def SetCountdownStage(countdownStartTimeInput):
    global countdownState, countdownStartTime, countdownTime
    countdownState = False # Reassuring
    countdownStartTime = countdownStartTimeInput
    countdownTime = countdownStartTime
    timerSeconds = countdownStartTime % 60
    timerMinutes = countdownStartTime // 60
    
    timeString = pattern.format(timerMinutes, timerSeconds)
    # Update the countdownText Label with the updated time
    countdownText.configure(text=timeString)
    challengeTimeLabel.configure(text=timeString)
    
    #update the wedge on canvas
    currentAngle=90
    DrawWedgeOnCanvas(currentAngle)

def SetStage1():
    titleText = "The Opponent Challenges the Reporter"
    countdownStartTime = 1*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText)

def SetStage2():
    titleText = "The Reporter accepts or rejects the challenge"
    countdownStartTime = 2*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage
    
def SetStage3():
    titleText = "Preparation of the Reporter"
    countdownStartTime = 5*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage
        
def SetStage3():
    titleText = "Presentation of the report"
    countdownStartTime = 10*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage4():
    titleText = "Questions from the opponent"
    countdownStartTime = 2*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage5():
    titleText = "Preparation for the opponent"
    countdownStartTime = 3*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage 

def SetStage6():
    titleText = "The opponent's speech"
    countdownStartTime = 5*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage7():
    titleText = "Discussion between the reporter and opponent"
    countdownStartTime = 5*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage8():
    titleText = "Questions from the reviewer"
    countdownStartTime = 2*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage9():
    titleText = "Preparation for the reviewer"
    countdownStartTime = 1*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage10():
    titleText = "The reviewer's speech"
    countdownStartTime = 3*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage11():
    titleText = "Discussion on stage"
    countdownStartTime = 4*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage12():
    titleText = "General discussion between the teams"
    countdownStartTime = 5*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage13():
    titleText = "Concluding remarks of the reporter"
    countdownStartTime = 1*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage14():
    titleText = "Questions of the jury"
    countdownStartTime = 6*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage15():
    titleText = "Putting marks"
    countdownStartTime = 1*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage

def SetStage16():
    titleText = "Jury remarks"
    countdownStartTime = 4*60 # time in seconds
    SetCountdownStage(countdownStartTime) # make the time adjustment
    presentationTextLabel.configure(text=titleText) # update text presenting stage


    
countdownState = False # set start state of timer to false.    
countdownStartTime = 10 # initialise
### Start of GUI part ###
master = tk.Tk() #define master tk object

#countdownStartTime = 10 #### TestTime
countdownTime = countdownStartTime
pattern = '{0:02d}:{1:02d}' # the pattern format for the timer to ensure 2 digits


# set the background color, given from variable at start
master.configure(background=defaultBackgroundColor)


##########################
### Sponsor image to left (thought of as a combined image, preferable in .gif format else use ImageTk
#########################

sponsImage = tk.PhotoImage(file=leftSponsImagePath)

sponsLabel = tk.Label(master, image = sponsImage)
sponsLabel.grid(row=0 ,column = 0, columnspan=2, rowspan=2)

# add fields for reporter etc.
#reporter
reporterLabel = tk.Label( master, text= "Reporter",font=('Courier New',16))
reporterLabel.grid(row=6,column=0)
reporterLabel.configure(background=defaultBackgroundColor)

reporterEntry = tk.Entry( master, bd=5, font=('Courier New',16))
reporterEntry.grid( row=6,column=1)
reporterEntry.configure(background=defaultBackgroundColor)

#Opponent
opponentLabel = tk.Label( master, text= "Opponent",font=('Courier New',16))
opponentLabel.grid(row=7,column=0)
opponentLabel.configure(background=defaultBackgroundColor)

opponentEntry = tk.Entry( master, bd=5, font=('Courier New',16) )
opponentEntry.grid( row=7,column=1)
opponentEntry.configure(background=defaultBackgroundColor)

#Reviewer
reviewerLabel = tk.Label( master, text= "Reviewer",font=('Courier New',16))
reviewerLabel.grid(row=8,column=0)
reviewerLabel.configure(background=defaultBackgroundColor)

reviewerEntry = tk.Entry( master, bd=5, font=('Courier New',16))
reviewerEntry.grid( row=8,column=1 )
reviewerEntry.configure(background=defaultBackgroundColor)




# Call DrawWedgeOnCanvas first time for initial setup
currentAngle = 90
if ( installedMatplotlib ): # doesn't draw in case matplotlib isn't installed
    DrawWedgeOnCanvas(currentAngle)
    
#####################
# frame for bottoms and writing, (at the bottom and right
##################

# create string for countdownTimer startTime
timerSeconds = countdownStartTime % 60
timerMinutes = countdownStartTime // 60        
timeString = pattern.format(timerMinutes, timerSeconds)
        
        
# Digital clock present time
#challengeTimeVar = "01:00" # this should be coupled to choice of stage
challengeTimeVar = timeString
challengeTimeLabel = tk.Label(master, text=challengeTimeVar, font=('Courier New',18) )
challengeTimeLabel.grid(row=8, column=3, rowspan=2)
challengeTimeLabel.configure(background=defaultBackgroundColor)

challengeTimeTextLabel = tk.Label(master, text="ChallengeTime", font=('Courier New',18) )
challengeTimeTextLabel.grid(row=6, column=3, rowspan=2)
challengeTimeTextLabel.configure(background=defaultBackgroundColor)


# Digital clock countdown
digitalCountdownVar = timeString
countdownText = tk.Label(master, text=digitalCountdownVar, font=('Courier New',18))
countdownText.grid(row=8, column=4, rowspan=2)
countdownText.configure(background=defaultBackgroundColor)

countdownTextLabel=tk.Label(master, text="Countdown", font=('Courier New',18))
countdownTextLabel.grid(row=6, column=4, rowspan=2)
countdownTextLabel.configure(background=defaultBackgroundColor)


# Presentation of current phase
presentationTextLabel = tk.Label(master, text= presentationText, font=('Courier New',28))
presentationTextLabel.grid(row=4, column=2, columnspan=2)
presentationTextLabel.configure(background=defaultBackgroundColor)

## Control Buttons ##

#startButton
startButton = tk.Button(master=master, text='Start', command= StartCountdown )
startButton.grid(row=5, column=7)
startButton.configure(background=defaultBackgroundColor)

#PauseButton
pauseButton = tk.Button(master=master, text='Pause', command= PausCountdown)
pauseButton.grid(row=6, column=7)
pauseButton.configure(background=defaultBackgroundColor)

#Reset button
resetButton = tk.Button(master=master, text='Reset', command= ResetCountdown)
resetButton.grid(row=6, column=8)
resetButton.configure(background=defaultBackgroundColor)

#Quit button
quitButton = tk.Button(master=master, text='Quit', command=_quit)
quitButton.grid(row=8,column=8)
quitButton.configure(background=defaultBackgroundColor)

###############################
## Top menu configuration ##
###########################3

menubar = tk.Menu(master)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_separator()

filemenu.add_command(label="Exit", command=_quit)
menubar.add_cascade(label="File", menu=filemenu)


stagemenu = tk.Menu(menubar, tearoff=0)
stagemenu.add_command(label="1:The Opponent Challenges the Reporter", command=SetStage1 )
stagemenu.add_command(label="2:The Reporter accepts or rejects the challenge", command=SetStage2 )
stagemenu.add_command(label="3:Preparation of the Reporter", command=SetStage3 )
stagemenu.add_command(label="4:Questions from the opponent", command=SetStage4 )
stagemenu.add_command(label="5:Preparation for the opponent", command=SetStage5 )
stagemenu.add_command(label="6:The opponent's speech", command=SetStage6 )
stagemenu.add_command(label="7:Discussion between the reporter and opponent", command=SetStage7 )
stagemenu.add_command(label="8:Questions from the reviewer", command=SetStage8 )
stagemenu.add_command(label="9:Preparation for the reviewer", command=SetStage9 )
stagemenu.add_command(label="10:The reviewer's speech", command=SetStage10 )
stagemenu.add_command(label="11:Discussion on stage", command=SetStage11 )
stagemenu.add_command(label="12:General discussion between the teams", command=SetStage12 )
stagemenu.add_command(label="13:Concluding remarks of the reporter", command=SetStage13 )
stagemenu.add_command(label="14:Questions of the jury", command=SetStage14 )
stagemenu.add_command(label="15:Putting marks", command=SetStage15 )
stagemenu.add_command(label="16:Jury remarks", command=SetStage16 )

menubar.add_cascade(label="Stage", menu=stagemenu)

master.config(menu=menubar)

############################




# change column behaviour for scaling
master.columnconfigure(3, weight=1)
master.columnconfigure(3, pad=7)
master.columnconfigure(6, weight=1)
master.rowconfigure(0, weight=1)
master.rowconfigure(1, weight=1)
master.rowconfigure(4, pad=7)


update_countdown() # update the countdown

# start the GUI loop
master.mainloop()
