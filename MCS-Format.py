from easygui import *
import sys
import glob
from filemanager import FileManager

global fm 

def selectRoot():
    global fm
    rootSearchPath = diropenbox(msg="Choose a directory containing .asm files")
    fm = FileManager(rootSearchPath)
    


def main(): 
    msg = "Thank you for using MCS-Format!\nMCS-Format will seach sub-folders recursively for .asm files.\n\nPress continue to select a directory containing .asm files for formatting."
    title = "MCS-Format"
    if ccbox(msg, title):     # show a Continue/Cancel dialog
        selectRoot()
    else:  # user chose Cancel
        sys.exit(0)
main()