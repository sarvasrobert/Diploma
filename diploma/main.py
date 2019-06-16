#!C:\Users\Robert\Anaconda3\python.exe

#####################################################################
'''  Neccessary Imports  '''

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
    
try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1
    
if py3 ==0:
    import tkFileDialog as filedialog
else:
    from tkinter import filedialog as filedialog

import sys
#import pymedia
from tkinter import dnd
import time
import os
import main_support
import numpy as np
import cv2
import PIL
import imutils
import importlib
from PIL import Image,ImageTk,ImageFilter,ImageOps,ImageDraw
from matplotlib import pyplot as plt


import sys
print(sys.version)

#########Import OSVOS ###############
#text = os.popen("dir")
#
##os.popen("activate tf15")
import tensorflow as tf

#sys.path.append('C:/Users/Robert/Desktop/diploma/test-video1/osvos')
#import osvos_demo
#moduleName = input(osvos_demo.py)
#importlib.import_module(moduleName)

#####################################################################
'''  Top Level functions for opening and closing whole application, whitch is stored in MainGUI class  '''

def start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = main_support.MainGUI (root)
    main_support.init(root, top)
    root.mainloop()

w = None
def create_New_GUI(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = main_support.MainGUI (w)
    main_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_MainGUI():
    global w
    cv2.destroyAllWindows();
    w.destroy()
    w = None


#####################################################################
''' Main GUI class that cover all the functionality and operations '''



if __name__ == '__main__':  
    start_gui()


