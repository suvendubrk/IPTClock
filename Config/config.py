###################################################
#  This file contains variables used for tweaking #
#  such as backgroundcolor filepaths etc.         #
###################################################

fps = 1 # used for timer to set update frequency

defaultBackgroundColor = None  # 'blue'    # String, following tkinter naming. color used for background, buttons and labels etc. NOT color behind wedge, use "None" without "" to get system default

wedgeBackgroundColor = None  # '#13235b' #String, following matplotlib naming.  color of the wedge background (for example to adhere to present year's color scheme. None defaults to Tkinter color from defaultBackgroundColor

clockColors = ['#7DC7EE', '#FED812', '#d32c2c', '#864da0']  # List of colors for the clock to cycle through

# Path to sponsor image [Presently PNG!], if using tkinter and label, it has to be in GIF and if we use matplotlib it has to be in PNG.
leftSponsImagePath = './Images/Sponsors/sponsors.png' # './testPicture.gif'  # './ponyAndDuck.gif'

pathToSoundFile = ''#'./Audio/theDuckSong2.wav'  # If left empty nothing happens, requires [.wav]

stagesPath = "./Stages/stages.txt"  # Stages config path

# To be introduced...:
# defaultFont = # string deciding the standard font
# defaultFontSize =  # integer, fontsize of text

