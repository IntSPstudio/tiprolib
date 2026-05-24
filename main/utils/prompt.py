#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from config import CLI_SC
import os

#CLEAR SCREEN
def cli_screen_clear():
    if CLI_SC == True:
        os.system('cls' if os.name == 'nt' else 'clear')