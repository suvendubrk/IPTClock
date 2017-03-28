###################################################
#  This file contains variables used for tweaking #
#  such as backgroundcolor filepaths etc.         #
###################################################

fps = 1 # used for timer to set update frequency

defaultBackgroundColour = '#FFFFFF'  # 'blue'    # String, following tkinter naming. colour used for background, buttons and labels etc. NOT colour behind wedge, use "None" without "" to get system default

wedgeBackgroundColour = '#FFFFFF'# None  # '#13235b' # String, following matplotlib naming.  colour of the wedge background (for example to adhere to present year's colour scheme. None defaults to Tkinter colour from defaultBackgroundColour

textColour = 'black'  # String, following tkinter naming. colour used for text colour. Use "None" without "" to get system default.

clockColours = ['#7DC7EE', '#FED812', '#d32c2c', '#864da0']  # List of colours for the clock to cycle through

# Path to sponsor image [Presently PNG!], if using tkinter and label, it has to be in GIF and if we use matplotlib it has to be in PNG.
leftSponsImagePath = './Images/Sponsors/sponsors.png' #./Images/Sponsors/sponsors.png' # './testPicture.gif'  # './ponyAndDuck.gif'

pathToSoundFile = ''#'./Audio/theDuckSong2.wav'  # If left empty nothing happens, requires [.wav]

stagesPath = "./Stages/stages.txt"  # Stages config path

# To be introduced...:
defaultFont = 'Courier New' # string deciding the standard font


