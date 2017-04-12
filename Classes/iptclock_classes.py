#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
if sys.version_info[0] < 3:
    usePython3 = False
else:    
    usePython3 = True

from Config.config import * # imports configuration variables
import math

import matplotlib as mpl
mpl.use('TkAgg') # needs to be called before plt


try:
    import pyaudio
    installedPyaudio = True
except ImportError:
    installedPyaudio = False


if usePython3:
    import tkinter as tk
    import _thread # in order to utilize threads # the threading that is used is written for python 3

else:
    import Tkinter as tk
    installedPyaudio = False # to avoid calling python3 specific commands.
    import copy
    
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import time

# imports pillow as an alternative way of displaying images.
from PIL import Image, ImageTk


# check if we use audio or not (.wave format)

if installedPyaudio:
    import wave

# import classes


    

###############
# Timer Class #
###############
class Timer():
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

    def set_time(self,time):
       self._set_time(time)

          
###############
# Stage Class #
###############

#########################
# Import stage Settings #
########################
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
        if usePython3:
            return self._stages.copy()
        else:
            return copy.copy(self._stages)


###############
# Clock Class #
###############

# first some functions...

def create_clock_labels(tkLabel):
    # Digital clock present time

    # Digital clock countdown
    countdownText = tk.Label(tkLabel, text='', font= tkLabel.customFontDigitalClock)
    countdownText.grid(row=1, column=2, columnspan=3)
    countdownText.configure(background=defaultBackgroundColour, fg= textColour)

    # Presentation of current phase
    wrapLength = 350
    presentationTextLabel = tk.Label(tkLabel, text='', font=tkLabel.customFontStage, wraplength= wrapLength)
    presentationTextLabel.grid(row=9, column=2, columnspan=3, sticky="EWS")
    presentationTextLabel.configure(background=defaultBackgroundColour, fg= textColour)

    return countdownText, presentationTextLabel, wrapLength


def create_clock_canvas(tkHandle,wedgeBgColour):
#    fig = plt.figure(figsize=(16, 16), edgecolor=None, facecolor=wedgeBgColour)
    fig = plt.figure(figsize=(16, 16), edgecolor = None, facecolor=wedgeBackgroundColour)
    ax = fig.add_subplot(111)
#    ax.set_axis_bgcolor(None) ###
#    ax.set_facecolor(None)  #######
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect(1)  # similar to "axis('equal')", but better.
    ax.axis('off')  # makes axis borders etc invisible.

    canvas = FigureCanvasTkAgg(fig, master=tkHandle)
#    canvas.get_tk_widget().configure(highlightthickness=0, highlightcolor=None)
    canvas.show()
   
    canvas.get_tk_widget().grid(row=2, column=2, columnspan=3, rowspan=7)  # , sticky=tk.N)
    return ax, fig, canvas


def get_backgroundColour():        
        # Find default background colour and check in case we use it
        defaultbgColour = self._tkHandle.cget('bg')  # find system window default colour
        bgRGB = self._tkHandle.winfo_rgb(self.defaultbgColour)
        bgRGB = (bgRGB[0]/(256**2), bgRGB[1]/(256**2), bgRGB[2]/(256**2))

        if wedgeBackgroundColour is None:
            self.wedgeBackgroundColour = bgRGB      


class Clock:
    def __init__(self, tkHandle):
#        self.low_health_ratio =
        self._low_health_time = 15 # time left in second for activating low health mode
        self.is_low_health = False # boolean controlling low health mode
        self._tkHandle = tkHandle
        self.stage = Stage()
        self.timer = Timer()
        self.clock_graphics = ClockGraphics(self._tkHandle)
        self.startPlayingSongTime = 55 # time in seconds when death mode sound is played

        self.countdownText, self.presentationTextLabel, self.wrapLength = create_clock_labels(self._tkHandle)  # orig on LH self.challengeTimeLabel

        self._update_stage_dependencies()

    # To start the countdown
    def start(self):
        self.timer.start()

    # To pause the countdown
    def pause(self):
        self.timer.pause()

    # To reset the countdown to startTime
    def reset(self):

        # resets low health mode
        self.is_low_health = False
        
        # reset the timer
        self.timer.reset()

        # Update the countdownText Label with the updated time
        self.countdownText.configure(text=self.timer.string())

        # reset the clock graphics
        self.clock_graphics.reset()

    
    # Function playing song at time    
    def PlayASoundFile(self, pathToSoundFile):
        if ( installedPyaudio ):
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
#            angle = -360 * ((self.timer.start_time() - self.timer.time()) / self.timer.start_time())
            angle = -360 * ((self.timer.start_time() - self.timer.time()) / float(self.timer.start_time()) ) # added float since python2 returns int else.

            self.clock_graphics.set_angle(angle)

            # check for countdown time for activating "low health mode"
            if self.timer.time() < (self._low_health_time +2) : # +1 since we update after time update. another +1 to activate at the specified time.
                # check if low health mode is activated
                if not self.is_low_health:
                    self.is_low_health = True # update boolean so we don't call it more than once
                    self.low_health_mode()            

        # Call the update() function after 1/fps seconds
        dt = (time.time() - t0) * 1000
        time_left = max(0, int(1000 / fps - dt))
        self._tkHandle.after(time_left, self.update)

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
       # self.challengeTimeLabel.configure(text=self.timer.string())
        self.reset()
        self.presentationTextLabel.configure(text=self.stage.description())  # update text presenting stage

    def set_stage_startTime(self, start_time):
        # Set the present countdown time of the timer
        self.reset()
        self.timer.set_time(self.stage.time() - start_time)
        self.refresh()
       

    def refresh(self):
         # Update the countdownText Label with the updated time
        self.countdownText.configure(text=self.timer.string()) 

        angle = -360 * ((self.timer.start_time() - self.timer.time()) / float(self.timer.start_time()) ) # added float since python2 returns int else.

        self.clock_graphics.set_angle(angle)

    def low_health_mode(self):
        background_colour = 'red' # colour of last wedge part in low health
        self.clock_graphics.set_wedge_background_colour(background_colour)
        
        # for playing low health sound
#            if usePython3:
#                    _thread.start_new_thread(self.PlayASoundFile, (pathToSoundFile,))

#######################
# ClockGraphics Class #
#######################
class ClockGraphics:
    def __init__(self, tkHandle):
        self._tkHandle = tkHandle
        # Definition of initial clock state/position
        self._clock_center = [0, 0]
        self._clock_reference_angle = 90
        self._clock_radius = 0.9
        self._angle = 90 #0

        # Check colours
        self._set_backgroundColour()
        
        # Creation of clock graphical elements
        self._ax, self._fig, self._canvas = create_clock_canvas(self._tkHandle, self.wedgeBackgroundColour)
        self._wedge = self._create_wedge(2)
        self._backgroundDisc = self._create_circle(1, True)
        self._perimiterCircle = self._create_circle(3, False)

        # set colours
        self._colours = [self.wedgeBackgroundColour] + clockColours  # [wedgeBackgroundColour, wedgeColour, 'red', 'purple']
       
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

    def _switch_colours(self):
        lap = int(abs(self._angle - 1e-3)/360)
        if lap < len(self._colours)-1:
            wedge_colour = self._colours[lap+1]
            background_colour = self._colours[lap]
        else:
            wedge_colour = self._backgroundDisc.get_facecolor()
            background_colour = self._wedge.get_facecolor()
            
        self._wedge.set_facecolor(wedge_colour)
        self._backgroundDisc.set_facecolor(background_colour)
         

    def set_angle(self, new_angle):
        self._angle = new_angle
        self.update()

    def update(self):
        if self._isTwelve():
            self._switch_colours()
        self._update_wedge()
        self._updateCanvas()

    def reset(self):
        self.set_angle(0)

    def _set_backgroundColour(self):        
        # Find default background colour and check in case we use it
        self.defaultbgColour = self._tkHandle.cget('bg')  # find system window default colour
        bgRGB = self._tkHandle.winfo_rgb(self.defaultbgColour)
        bgRGB = (bgRGB[0]/(256**2), bgRGB[1]/(256**2), bgRGB[2]/(256**2))

        if wedgeBackgroundColour is None:
            self.wedgeBackgroundColour = bgRGB
        else:
            self.wedgeBackgroundColour = wedgeBackgroundColour

    def set_wedge_background_colour(self, background_colour):
        self._backgroundDisc.set_facecolor(background_colour)
        
###########
# Timeout #
###########

#####################
# TimoutTimer Class #
#####################

class TimeoutTimer():
    # A slighly modded version of Timer class.
    def __init__(self):
        self._tick_state = False
        self._start_time = 0
        self._time = 0
        self._string = ''

        self._string_pattern = '{0:02d}:{1:02d}:{2:02d}'  # the pattern format for the timer to ensure 2 digits
        self._time_step = float(1)/10 #1/fps # added float for python 2 compatibility

        self.set_timer(self._start_time)

    def _update_string(self):
        seconds = int(abs((self._time + 1e-3)) % 60)
        minutes = int(abs((self._time + 1e-3 ) ) // 60)
        centiseconds = int(math.ceil(abs(self._time*100-1e-3 ) ) % 100  )
        
        # fixes the countdown clock when deadline is passed
        if self._time < 0:
                self._string = '-' + self._string_pattern.format(minutes, seconds, centiseconds)
        else:
            self._string = self._string_pattern.format(minutes, seconds, centiseconds)

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

    def set_time_step(self, fps):
        self._time_step = 1/fps


#################        
# Timeout Class #
#################

class TimeoutClass:    
    def __init__(self, clockHandle):
        self._clock_handle = clockHandle # handle for the clock class, used for pause/start.
        self._master_handle  = self._clock_handle._tkHandle
        self.fps = 10 # value controlling timesteps displayed in dountdown.
        

        self.timeoutTime = 60 # [s], the time of the Timeout.
        self.timerStopTime = 0 # the time at which the timout timer should stop.
        self.timer = TimeoutTimer()
        self.timer.set_timer(self.timeoutTime)
        self.timeoutState = True
        self.timer.start()

        # check if clock is running
        self.tick_state = self._clock_handle.timer._tick_state             
        self._clock_handle.pause() # pause clock
        
        
    def setupTimeout(self):
        # create and positions the pop up frame
        self.top = tk.Toplevel()
        self.top.title("TIMEOUT!")
        self.top.configure(bg= defaultBackgroundColour)

      
        self.msg = tk.Label(self.top, text=self.timer.string,  font=('Courier New', 60) )
        self.msg.pack(fill='x')
        self.msg.configure(bg=defaultBackgroundColour, fg= textColour)

        self.button = tk.Button(self.top, text="Dismiss", command=self.exit_timeout)
        self.button.configure(bg = defaultBackgroundColour, fg= textColour )
        self.button.pack()
        self.top.protocol("WM_DELETE_WINDOW", self.exit_timeout) # if push x on border
        self.centreTop(self.top)
       

  # function updating the time
    def update(self):       
        # Every time this function is called,
        # decrease timer with one second

        t0 = time.time()

        if self.timer.isTicking():
            # Update the countdownText Label with the updated time
            self.msg.configure(text=self.timer.string())

            self.timer.tick() # new time step
           

            # Call the update() function after 1/fps seconds
            dt = (time.time() - t0) * 1000

            time_left = max(0, int(1000 / self.fps - dt))
            #        time_left = max(0, int(1000 / float(self.fps) - dt))
            
            self._master_handle.after(time_left, self.update)

            # check exit criteria
            if self.timer.time() < self.timerStopTime :
                
                # terminate countdown and unpause main clock       
                self.exit_timeout()
  
			

    def exit_timeout(self):
	        # check so that we don't start the clock if it wasn't running before timeout
        self.timer.pause() # needed to avoid calls to non existen msg
        if self.tick_state:
            self._clock_handle.start()
	
        self.top.destroy()
 
    def centreTop(self, toplevel):
        # centering the top widget
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


###################
# SponsImageClass #
###################

class SponsImage():
    # class displaying a frame containing
    # a image drawn on canvas using matplotlib
    def __init__(self,tkHandle):
        self._tkHandle = tkHandle
        self._sponsImage = leftSponsImagePath # must be PNG
        self.img = mpimg.imread( self._sponsImage )#'./ponyAndDuck.png') # converts/load image
        self.widthRatioOfImage = 0.35 # how much of the screen that is sponsImage
        self._determine_pixeldistance()
        self._fig, self._canvas, self._plt  = self._create_sponsImage_canvas()
        

    def _updateCanvas(self):
        # Tkinter need to redraw the canvas to actually show the new updated matplotlib figure
        self._canvas.draw()

    def _determine_pixeldistance(self):
        #determines how many mm there is between the pixels
        widthmm, heightmm, width, height = self.screen_dimensions()
        self.pixDist_width = widthmm*1.0/width
        self.pixDist_height = heightmm*1.0/height
       

    def _create_sponsImage_canvas(self):
        widthmm, heightmm, width, height = self.screen_dimensions()

        # inch convert
        widthInch =  widthmm* 0.0393700787 * self.widthRatioOfImage
        heightInch = heightmm * 0.0393700787

        sponsFig = plt.figure(figsize =(widthInch,heightInch), dpi=200 ,edgecolor=None, facecolor = defaultBackgroundColour )#facecolor=wedgeBackgroundColour)        
        
        imgplot = plt.imshow(self.img, interpolation='bilinear')
        plt.axis('off') # removes labels and axis, numbers etc.
        plt.tight_layout(pad=0, w_pad=0, h_pad=0) # removes padding round figure

        # Create own frame for the canvas     
        self.SponsFrame = tk.Frame(self._tkHandle)
        self.SponsFrame.config(bg= defaultBackgroundColour)
        sponsCanvas = FigureCanvasTkAgg(sponsFig, master=self.SponsFrame)
        sponsCanvas.get_tk_widget().configure(background= defaultBackgroundColour)
        sponsCanvas.show()

        # align frame and let canvas expand
        self.SponsFrame.grid(row=0, column=0, columnspan=1, rowspan=14 , sticky='NW') 
   #     sponsCanvas.get_tk_widget().grid(row=0, column=0, columnspan=1, rowspan=14 , sticky='NWES')
        sponsCanvas.get_tk_widget().pack(expand=True)
        plt.gca().set_position([0,0,1,1])
        return sponsFig, sponsCanvas, imgplot 


    def screen_dimensions(self):
        #returns size of screen in mm and pixels     
        widthmm = self._tkHandle.winfo_screenmmheight() #returns size of master object in mm
        heightmm = self._tkHandle.winfo_screenmmwidth()

        width = self._tkHandle.winfo_screenheight() #returns size of master object in mm
        height = self._tkHandle.winfo_screenwidth()        
        return widthmm, heightmm, width, height

    def canvas_size(self):
        widthPix = self._canvas.winfo_width()
        heightPix = self._canvas.winfo_height()
        return widthPix, heightPix


    def updateFigSize(self):
        widthPix, heightPix =  self.SponsFrame.winfo_width(), self.SponsFrame.winfo_height()
 
        widthmm = widthPix * self.pixDist_width
        heightmm = heightPix * self.pixDist_height
               
        # inch convert
        widthInch =  widthmm* 0.0393700787 # * self.widthRatioOfImage
        heightInch = heightmm * 0.0393700787
        
        self._updateCanvas()


        
#############################################################
# Sponsor Image class  using Pillow for scaling and display #
#############################################################
        
class SponsImagePillow():
    # Class displaying a frame containing a (sponsor) image
    # using tkinter and PIL.
    def __init__(self,tkHandle):
        self._tkHandle = tkHandle
        self._sponsImage = leftSponsImagePath # Can be any format supported by PIL
        self.image2_orig = Image.open(leftSponsImagePath) # keep original
        self.image2 = self.image2_orig.copy() # create copy image to work with

        # create the frame used to display image in  
        self.SponsFrame = tk.Frame(self._tkHandle)
        
        # align frame and let it expand
        self.SponsFrame.grid(row=0, column=0, columnspan=1, rowspan=14 , sticky='WESN')

        self.SponsFrame.config(bg= defaultBackgroundColour)

        self.image_size = self.get_FrameSize() # get given size for frame.

        # convert initial image into tk compatible format
        self.tk_image = ImageTk.PhotoImage( self.image2 )

        # create label containing image
        self.displayLabel = tk.Label(self.SponsFrame, image = self.tk_image)
        self.displayLabel.configure(bg= defaultBackgroundColour)
        self.displayLabel.grid(sticky='NWSE')

    def get_FrameSize(self):        
        # Returns the size of the frame in pixels.
        # Will return 1x1 pixels if called before
        # frame is processed by geometry manager (here .grid)
        xsize, ysize = self.SponsFrame.winfo_width(), self.SponsFrame.winfo_height()
        size = [xsize,ysize]
        return size
        
    def updateFigSize(self):
        self.image_size = self.get_FrameSize()
        # makes copy of original to avoid recursive smaller images.
        self.image2 = self.image2_orig.copy()

        # downsize the original file
        self.image2.thumbnail(self.image_size, resample=Image.LANCZOS) # improve image by lanczosfilter

        self.tk_image = ImageTk.PhotoImage( self.image2 ) # convert resized file to tk readable format
        self.displayLabel.configure(image = self.tk_image) # update the displayed image


#######################
# Edit Frame class
######################
class EditFrame():
    def __init__(self,tkHandle):
        self.tk_handle = tkHandle
        self.hide_competitors = tk.IntVar() # for controling appearance of competitors
        self.hide_competitors.set(1)

        self.hide_buttons = tk.IntVar()
        self.hide_buttons.set(0)

        
        self._create_top_frame()
        self.centerTop(self.top) # center the popup

        
        self.toggle_show_competitors()

    def _create_top_frame(self):        
        # create and positions the pop up frame
        self.top = tk.Toplevel()
        self.top.title("Edit")
        self.top.configure(bg= defaultBackgroundColour)
        self.top.protocol("WM_DELETE_WINDOW", self.exit) # if push x on border
        
        # Stage
        self.stageLabel = tk.Label(self.top, text = "Stage font size:",anchor='w')
        self.stageLabel.grid(column=0,row=0,sticky='EW')
        self.stageLabel.configure(background=defaultBackgroundColour, fg= textColour)

        
       # self.stageSpinBox = tk.Spinbox(self.top, from_=1, to=self.tk_handle.maxStageFontSize, textvariable = self.tk_handle.stageFontSize)
        self.stageSpinBox = tk.Spinbox(self.top, from_=1, to=200, textvariable = self.tk_handle.stageFontSize)
        self.stageSpinBox.grid(column=1, row=0)
        self.stageSpinBox.configure(background=defaultBackgroundColour, fg= textColour)
        
        # Digital Clock
        self.clockLabel = tk.Label(self.top, text = "Clock font size:",anchor='w')
        self.clockLabel.grid(column=0,row=1,sticky='EW')
        self.clockLabel.configure(background=defaultBackgroundColour, fg= textColour)
        
        self.clockSpinBox = tk.Spinbox(self.top, from_=1, to=200, textvariable = self.tk_handle.digitalClockFontSize)#self.tk_handle.stageFontSize)
        self.clockSpinBox.grid(column=1, row=1)
        self.clockSpinBox.configure(background=defaultBackgroundColour, fg= textColour)
        
        # Competitor labels
        self.competitorLabel = tk.Label(self.top, text = "Competitor font size:",anchor='w')     
        self.competitorLabel.grid(column=0,row=2,sticky='EW')
        self.competitorLabel.configure(background=defaultBackgroundColour, fg= textColour)
        
        self.competitorSpinBox = tk.Spinbox(self.top, from_=1, to=200, textvariable = self.tk_handle.competitorFontSize)#self.tk_handle.stageFontSize)
        self.competitorSpinBox.grid(column=1, row=2)
        self.competitorSpinBox.configure(background=defaultBackgroundColour, fg= textColour)

        # Buttons font size         
        self.buttonLabel = tk.Label(self.top, text = "Button font size:",anchor='w', justify='left')
        self.buttonLabel.grid(column=0,row=3,sticky='EW')
        self.buttonLabel.configure(background=defaultBackgroundColour, fg= textColour)
        
        self.buttonSpinBox = tk.Spinbox(self.top, from_=1, to=200, textvariable = self.tk_handle.buttonFontSize)#self.tk_handle.stageFontSize)
        self.buttonSpinBox.grid(column=1, row=3)
        self.buttonSpinBox.configure(background=defaultBackgroundColour, fg= textColour)


        # Tick boxes        
        self.competitorHideTick = tk.Checkbutton(self.top, text="Hide competitors", var = self.hide_competitors , command= self.toggle_show_competitors)
        self.competitorHideTick.grid(column = 2, row = 2)
        self.competitorHideTick.configure(background=defaultBackgroundColour, fg= textColour)

        self.ButtonsHideTick = tk.Checkbutton(self.top, text="Hide buttons", var = self.hide_buttons , command= self.toggle_show_buttons)
        self.ButtonsHideTick.grid(column = 2, row = 1)
        self.ButtonsHideTick.configure(background=defaultBackgroundColour, fg= textColour)


        
        
        # Sponsor image width
        self.sponsImageLabel = tk.Label(self.top, text = "Sponsor image minimum width:",anchor='w', justify='left')
        self.sponsImageLabel.grid(column=0,row=4,sticky='EW')
        self.sponsImageLabel.configure(background=defaultBackgroundColour, fg= textColour)

        self.sponsImageSpinBox = tk.Spinbox(self.top, from_=1, to=1000, textvariable = self.tk_handle.sponsWidth)
        self.sponsImageSpinBox.grid(column=1, row=4)
        self.sponsImageSpinBox.configure(background=defaultBackgroundColour, fg= textColour)

        self.updateWidthButton = tk.Button(self.top, text="Update image", command=self.update_sponsWidth)
        self.updateWidthButton.grid(column=2, row = 4)
        self.updateWidthButton.configure(background=defaultBackgroundColour, fg= textColour)
        
        
        
        ## Competitors ##
        # Reporter
        self.reporterLabel = tk.Label(self.top,  text="Reporter:", anchor='w')
        self.reporterLabel.grid(column=0, row= 5,sticky='we')
        self.reporterLabel.configure(background=defaultBackgroundColour, fg= textColour)

        self.reporterStrVar = tk.StringVar()
        self.reporterStrVar.set(self.tk_handle.reporterNameLabel.cget('text') )
        self.reporterEntry = tk.Entry(self.top, text =  self.reporterStrVar )
        self.reporterEntry.grid(column=1, row=5, sticky='we', columnspan=2)
        self.reporterEntry.configure(background=defaultBackgroundColour, fg= textColour)

        # Opponent
        self.opponentLabel = tk.Label(self.top,  text="Opponent:", anchor='w')
        self.opponentLabel.grid(column=0, row= 6,sticky='we')
        self.opponentLabel.configure(background=defaultBackgroundColour, fg= textColour)

        self.opponentStrVar = tk.StringVar()
        self.opponentStrVar.set(self.tk_handle.opponentNameLabel.cget('text') )
        self.opponentEntry = tk.Entry(self.top, text =  self.opponentStrVar )
        self.opponentEntry.grid(column=1, row=6, sticky='we', columnspan=2)
        self.opponentEntry.configure(background=defaultBackgroundColour, fg= textColour)

        # Reviewer
        self.reviewerLabel = tk.Label(self.top,  text="Reviewer:", anchor='w')
        self.reviewerLabel.grid(column=0, row= 7,sticky='we')
        self.reviewerLabel.configure(background=defaultBackgroundColour, fg= textColour)

        self.reviewerStrVar = tk.StringVar()
        self.reviewerStrVar.set(self.tk_handle.reviewerNameLabel.cget('text') )
        self.reviewerEntry = tk.Entry(self.top, text =  self.reviewerStrVar )
        self.reviewerEntry.grid(column=1, row=7, sticky='we', columnspan=2)
        self.reviewerEntry.configure(background=defaultBackgroundColour, fg= textColour)

        
        # buttons
        self.updateButton = tk.Button(self.top, text="Update text", command=self.update )
        self.updateButton.grid(column=0, row = 8)
        self.updateButton.configure(background=defaultBackgroundColour, fg= textColour)

        self.closeButton = tk.Button(self.top, text="Close", command=self.exit )
        self.closeButton.grid(column=0, row = 14,sticky='we')
        self.closeButton.configure(background=defaultBackgroundColour, fg= textColour,font= self.tk_handle.customFontButtons)

        self.resetButton = tk.Button(self.top, text="Reset font", command=self.reset_font )
        self.resetButton.grid(column=1, row = 8)
        self.resetButton.configure(background=defaultBackgroundColour, fg= textColour)
        


        # seperation line
        horizontalLine = tk.Label(self.top, text='-', background='darkgray', height=1, font=('Courier New', 1), borderwidth=0)
        horizontalLine.grid(row=9, column=0, columnspan=3, sticky='WE', pady=10)
        
        #### Control buttons ########

        
        self.startButton = tk.Button(master=self.top, text='Start', command=self.tk_handle.IPTClock.start, font= self.tk_handle.customFontButtons)
        self.startButton.configure(background=defaultBackgroundColour, fg= textColour)
        self.startButton.grid(column=1, row = 10,sticky='we')
        
        
         # Pause Button
        self.pauseButton = tk.Button(master=self.top, text='Pause', command=self.tk_handle.IPTClock.pause, font= self.tk_handle.customFontButtons)
        self.pauseButton.configure(background=defaultBackgroundColour, fg= textColour)
        self.pauseButton.grid(column=1, row = 11,sticky='we')

        
        # Fullscreen
        self.fullscreenButton = tk.Button(master=self.top, text='Fullscreen', command=self.fullscreen_toggle, font= self.tk_handle.customFontButtons)
        self.fullscreenButton.configure(background=defaultBackgroundColour, fg= textColour)
        self.fullscreenButton.grid(column=1, row = 13, sticky='we')

        
        # Previous Stage
        self.previousStageButton = tk.Button(master=self.top, text='<<', command=self.tk_handle.IPTClock.previous_stage, font= self.tk_handle.customFontButtons)
        self.previousStageButton.configure(background=defaultBackgroundColour, fg= textColour)
        self.previousStageButton.grid(column=0, row = 10, sticky='we')
        
        # Next Stage
        self.nextStageButton = tk.Button(master=self.top, text='>>', command=self.tk_handle.IPTClock.next_stage, font= self.tk_handle.customFontButtons)
        self.nextStageButton.configure(background=defaultBackgroundColour, fg= textColour)
        self.nextStageButton.grid(column=2,row = 10, sticky='we')
        
        # timeout
        def HandleReturn():
            return self.tk_handle.IPTClock, self.tk_handle

        
        # Timeout button
        self.timeoutButton = tk.Button(master=self.top, text='Timeout', command=self.timeoutButtonAction , font= self.tk_handle.customFontButtons)
        self.timeoutButton.configure(background=defaultBackgroundColour, fg= textColour)
        self.timeoutButton.grid(column=0, row = 12, sticky='we')

        # Reset button
        self.resetButton = tk.Button(master=self.top, text='Reset', command=self.tk_handle.IPTClock.reset, font= self.tk_handle.customFontButtons)
        self.resetButton.configure(background=defaultBackgroundColour, fg= textColour)
        self.resetButton.grid(column=2, row = 12, sticky='we')

        
        # Quit button
        self.quitButton = tk.Button(master=self.top, text='Quit', command=self.quitButtonAction, font= self.tk_handle.customFontButtons)
        self.quitButton.configure(background=defaultBackgroundColour, fg= textColour)
        self.quitButton.grid(column=2, row = 14, sticky='we')

        

        
    def _exit(self):
        self.top.destroy()

    def exit(self):
        self._exit()

    def reset_font(self):
        self.tk_handle.stageFontSize.set(self.tk_handle.customFontStage_orig)
        self.tk_handle.digitalClockFontSize.set(self.tk_handle.customFontDigitalClock_orig)
        self.tk_handle.competitorFontSize.set(self.tk_handle.customFontCompetitors_orig)
        self.tk_handle.buttonFontSize.set(self.tk_handle.customFontButtons_orig)
        
 
      
        # call window scaling
        if (self.tk_handle.fullscreen):
            screenWidth = self.tk_handle.winfo_screenwidth() 
        else:
            screenWidth = 640
            
        self.font_resize(int(screenWidth))
      
        


    def font_resize(self,screenWidthPixels):    
        # Determine present windowsize then upscale the font with the ration
        # between the present width and 480p (width 640 pixels) (choosen as base).
        # Uses original font sizes 
        
        widthPix = screenWidthPixels
        widthRatio = widthPix / 640.0
        
        fontSize = self.tk_handle.customFontCompetitors_orig
        fontSize = int( math.floor(fontSize*widthRatio) )
        self.tk_handle.customFontCompetitors.configure(size=fontSize)
        self.tk_handle.competitorFontSize.set(fontSize)
            
        fontSize = self.tk_handle.customFontButtons_orig
        fontSize = int( math.floor(fontSize*widthRatio) )
        #if (abs(fontSize) > 16):
        if fontSize < self.tk_handle.minButtonFontSize:
            fontSize = self.tk_handle.minButtonFontSize
        self.tk_handle.customFontButtons.configure(size=fontSize)
        self.tk_handle.buttonFontSize.set(fontSize)

        fontSize = self.tk_handle.customFontDigitalClock_orig
        fontSize = int( math.floor(fontSize*widthRatio) )
        self.tk_handle.customFontDigitalClock.configure(size=fontSize)
        self.tk_handle.digitalClockFontSize.set(fontSize)

    
        fontSize = self.tk_handle.customFontStage_orig
        fontSize = int( math.floor(fontSize*widthRatio) )
            
        # ensure stage fontsize is below imposed limit
        if( fontSize > self.tk_handle.maxStageFontSize):    
            self.tk_handle.customFontStage.configure(size=self.tk_handle.maxStageFontSize)
        else:
            self.tk_handle.customFontStage.configure(size=fontSize)
        self.tk_handle.stageFontSize.set(fontSize)        

            
        # scales the text wrap in stage presentation    
        wrapLength = math.floor( self.tk_handle.IPTClock.wrapLength * widthRatio  )
        self.tk_handle.IPTClock.presentationTextLabel.configure(wraplength= wrapLength)

        
   
    def update(self):
        # Updates the fontsize from configuration menu
        self.tk_handle.customFontStage.configure(size=self.tk_handle.stageFontSize.get())
        self.tk_handle.customFontDigitalClock.configure(size=self.tk_handle.digitalClockFontSize.get() )
        self.tk_handle.customFontCompetitors.configure(size=self.tk_handle.competitorFontSize.get() )
        self.tk_handle.customFontButtons.configure(size=self.tk_handle.buttonFontSize.get() )

              
        # update the competitors texts
        self.tk_handle.reporterNameLabel.configure(text=self.reporterStrVar.get())

        self.tk_handle.opponentNameLabel.configure(text=self.opponentStrVar.get())

        self.tk_handle.reviewerNameLabel.configure(text=self.reviewerStrVar.get())


    def update_sponsWidth(self):
         # update sponsImage width
        self.tk_handle.columnconfigure(0, weight=0, minsize = self.tk_handle.sponsWidth.get() )    # weight is changes here. Should give tighter padding        self.tk_handle.IPTSpons.updateFigSize()
        
		
    def centerTop(self, toplevel):
        # centering the top widget
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


    def toggle_show_competitors(self):
        
        if self.hide_competitors.get() == 1:
            self.tk_handle.competitorFrame.grid_forget()
        else:
             self.tk_handle.competitorFrameClass.position()
           


    def toggle_show_buttons(self):

        if (self.hide_buttons.get() ==1 ):
            self.tk_handle.ControlButtonFrameClass.forget_frame_position()
            self.tk_handle.ControlButtonFrameClass.hide_buttons()
        else:
            self.tk_handle.ControlButtonFrameClass.position_frame()
            self.tk_handle.ControlButtonFrameClass.position_buttons()

    def fullscreen_toggle(self):
        self.tk_handle.ControlButtonFrameClass.fullscreenToggle()

    def quitButtonAction(self):
        self.tk_handle.ControlButtonFrameClass.quitButtonAction()


    def timeoutButtonAction(self):
        self.tk_handle.ControlButtonFrameClass.timeoutButtonAction()
