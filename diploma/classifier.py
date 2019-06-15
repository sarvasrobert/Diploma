import sys

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

from tkinter import dnd
import sys
import time
import os
import scipy
import main_support
import numpy as np
import cv2
import PIL
import imutils
import importlib
import main
from PIL import Image,ImageTk,ImageFilter,ImageOps,ImageDraw
from matplotlib import pyplot as plt

'''
Class of local classifier 
'''


class Struct:
    def __init__ (self, *argv, **argd):
        if len(argd):
            # Update by dictionary
            self.__dict__.update (argd)
        else:
            # Update by position
            attrs = filter (lambda x: x[0:2] != "__", dir(self))
            for n in range(len(argv)):
                setattr(self, attrs[n], argv[n])


class ClassStruct (Struct):
    def __init__(self, x=0, y=0, w=0,h=0, image=None, mask=None, trimap=None, frameindex=None):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.frame = frameindex
        self.roi = image
        self.mask = mask
        #self.createtrimap(self.mask)
        self.trimap = trimap
        self.edge = None

    def showroi(self, image):
        image[self.y-self.height:self.y+self.height , self.x-self.width :self.x+ self.width] = self.roi

    def showalpha(self, image, alpha):
        #image[self.y-30:self.y+30,self.x-30:self.x+30] = alpha
        transparency = 0.6
        overlay_color = [0,0,255]
        #maska = np.zeros((self.mask.shape[0], self.mask.shape[1],3), np.uint8)
        #for y in range(len(self.mask)):
        #    for x in range(len(self.mask[y])):
        #        if self.mask[y,x] == 128:
        #            maska[y, x] = [1,1,1]

        #cv2.imshow('mask is ', self.mask)
        #cv2.imshow('trimap is ', self.trimap)
        #cv2.waitKey()
        only = cv2.subtract(self.mask, self.trimap) 
        self.edge = cv2.cvtColor(np.uint8(only), cv2.COLOR_BGR2GRAY)
        #cv2.imshow('only maybe is ', only)
        #cv2.waitKey()  
        image[self.y-self.height:self.y+self.height , self.x-self.width :self.x+ self.width, 0] = ( alpha) * image[self.y-self.height:self.y+self.height , self.x-self.width :self.x+ self.width, 0]# + alpha * (overlay_color * transparency + (1-transparency)*image[self.y-30:self.y+30, self.x-30:self.x+30, 0])
        image[self.y-self.height:self.y+self.height , self.x-self.width :self.x+ self.width, 1] = ( alpha) * image[self.y-self.height:self.y+self.height , self.x-self.width :self.x+ self.width, 1]# + alpha * (overlay_color * transparency + (1-transparency)*image[self.y-30:self.y+30, self.x-30:self.x+30, 1])#* only[:,:, 1])
        image[self.y-self.height:self.y+self.height , self.x-self.width :self.x+ self.width, 2] = ( alpha) * image[self.y-self.height:self.y+self.height , self.x-self.width :self.x+ self.width, 2]# + alpha * (overlay_color * transparency + (1-transparency)*image[self.y-30:self.y+30, self.x-30:self.x+30, 2])#* only[:,:, 0])
        # prvykraj = druhykraj = 1000
        # for y in range(0,59):
        #     for x in range(0,59):
        #         if (self.trimap[y , x,0] ==  128) & ((self.trimap[y, x+1,0]==255) | (self.trimap[y, x-1,0] == 255)):
        #             prvykraj = x
        #         if (self.trimap[y , x,0] ==  128) & ((self.trimap[y, x+1,0]==  0) | (self.trimap[y, x-1,0] ==   0)):
        #             druhykraj = x                
        # print('showalpha funguje ')
        # if (prvykraj != 1000) & (druhykraj != 1000):
        #     print('malo by to nieco robit')
        #     vzdialenost = abs(prvykraj - druhykraj)
        #     for y in range(self.y-30, self.y+30):
        #         for x in range(self.x-30, self.x+30):
        #             print('alpha je', alpha )
        #             transparency = 1 - (abs(x-prvykraj)/vzdialenost)
        #             image[y,x,0] = (1 - alpha[y,x]) * image[y,x, 0] + alpha[y,x] * (overlay_color[0]*transparency + (1-transparency)*image[y,x, 0])
        #             image[y,x,1] = (1 - alpha[y,x]) * image[y,x, 1] + alpha[y,x] * (overlay_color[1]*transparency + (1-transparency)*image[y,x, 1])
        #             image[y,x,2] = (1 - alpha[y,x]) * image[y,x, 2] + alpha[y,x] * (overlay_color[2]*transparency + (1-transparency)*image[y,x, 2])
        #             print('funguje na y', y ,'a x', x)
            #cv2.imshow('class alpha is', image)
            #cv2.waitKey()

        
    def createtrimap(self, mask):
        kernel = np.ones((3, 3), np.uint8)
        img_erode = cv2.erode(mask, kernel, iterations=2)
        img_dilate = cv2.dilate(img_erode, kernel, iterations=2)

        kernel = np.ones((3, 3), np.uint8)
        sure_fg = cv2.erode(img_dilate, kernel, iterations=3)
        #cv2.imshow('sure_fg of image (10,10) kernel', sure_fg)
        sure_bg = cv2.dilate(img_dilate, kernel, iterations=10)
        #cv2.imshow('sure_bg of image (10,10) kernel', sure_bg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        ret, thresh = cv2.threshold(unknown, 240, 255, cv2.THRESH_BINARY)
        unknown[thresh == 255] = 128 
        self.trimap = sure_fg + unknown      