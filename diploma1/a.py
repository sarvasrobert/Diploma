#! /usr/bin/env python

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
    
import sys
import pymedia
import time
import os
import a_support
import tkFileDialog
import numpy as np
import cv2
import PIL
import imutils
from PIL import Image,ImageTk,ImageFilter,ImageOps,ImageDraw
from matplotlib import pyplot as plt

#####################################################################
'''  Top Level functions for opening and closing whole application, whitch is stored in MainGUI class  '''

def start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = MainGUI (root)
    a_support.init(root, top)
    root.mainloop()

w = None
def create_New_GUI(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = MainGUI (w)
    a_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_MainGUI():
    global w
    cv2.destroyAllWindows();
    w.destroy()
    w = None


#####################################################################
''' Main GUI class that cover all the functionality and operations '''

class MainGUI:
    def __init__(self, top=None):
        '''This class configures and populates the main GUI window.
           top is the toplevel containing window.'''


        ''' FLAGS AND GLOBAL PARAMETERS'''
        self.RED = [0,0,255]         # rectangle color
        self.BLACK = [0,0,0]         # sure BG
        self.WHITE = [255,255,255]   # sure FG

        self.DRAW_BG = False         # turn on BG selction of pixels
        self.DRAW_FG = False         # turn on FG selction of pixels

        # setting up flags
        self.rect = (0,0,1,1)
        self.drawing = False         # flag for drawing curves
        self.rectangle = False       # flag for drawing rect
        self.rect_over = False       # flag to check if rect drawn
        self.rect_or_mask = 100      # flag for selecting rect or mask mode
        self.thickness = 3           # brush thickness


        foregroundcheck= False
        backgroundcheck= False        
        
        self.value = 10              # drawing initialized to FG
        self.rect_or_mask = 0        # flag for selecting rect or mask mode for Grabcut extraction
        self.pRect = True
        
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        self.top=top
        self.top.geometry("1680x790+376+61")
        self.top.title("Video Object Segmentation")
        self.top.configure(background="light slate gray")
        self.top.configure(highlightbackground="#d9d9d9")
        self.top.configure(highlightcolor="black")

        self.Canvas1 = Canvas(top)
        self.Canvas1.place(relx=0.005, rely=0.75, relheight=0.24, relwidth=0.99)
        self.Canvas1.configure(background="dark slate gray")
        self.Canvas1.configure(borderwidth="1")
        self.Canvas1.configure(highlightbackground="black")
        self.Canvas1.configure(highlightcolor="black")
        self.Canvas1.configure(insertbackground="black")
        self.Canvas1.configure(relief=RIDGE)
        self.Canvas1.configure(selectbackground="yellow") #(selectbackground="#c4c4c4")
        self.Canvas1.configure(selectforeground="black")
        #self.Canvas1.configure(width=681)

        self.panel = Label(top)  # initialize image panel
        self.panel.configure(background="black")
        self.panel.place(relx=0.01, rely=0.04, height=500, width=800)
        self.panel.bind("<ButtonPress-1>", self.on_button_press)
        self.panel.bind("<B1-Motion>", self.on_button_move)
        self.panel.bind("<ButtonRelease-1>", self.on_button_release)

        self.panel2 = Label(top)  # initialize image panel
        self.panel2.configure(background="black")
        self.panel2.place(relx=0.51, rely=0.04, height=500, width=800)
        
        self.Button1 = Button(top, command=self.load)
        self.Button1.place(relx=0.02, rely=0.84, height=43, width=78)
        self.Button1.configure(activebackground="light slate gray")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="black")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="white")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Load video''', foreground='white')
        #self.Button1.bind('<Button-1>',self.load)
    

        self.Button2 = Button(top, command=self.grabcut)
        self.Button2.place(relx=0.25, rely=0.84, height=43, width=78)
        self.Button2.configure(activebackground="light slate gray")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="black")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(state="disabled")
        self.Button2.configure(text='''GrabCUT''', foreground='white')
        #self.Button2.bind('<Button-2>')
        
        
        self.Button3 = Button(top, command=self.start)
        self.Button3.place(relx=0.11, rely=0.84, height=43, width=53)
        self.Button3.configure(activebackground="light slate gray")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="black")
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(state="disabled")
        self.Button3.configure(text='''|>''', foreground='white')
        #self.Button3.bind('<Button-3>',self.start)

        self.Button4 = Button(top, command=self.stop)
        self.Button4.place(relx=0.18, rely=0.84, height=43, width=53)
        self.Button4.configure(activebackground="light slate gray")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="black")
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(state="disabled")
        self.Button4.configure(text='''||''', foreground='white')
        #self.Button4.bind('<Button-4>',self.stop)

        self.Button5 = Button(top, command=self.fground)
        self.Button5.place(relx=0.32, rely=0.82, height=30, width=83)
        self.Button5.configure(activebackground="light slate gray")
        self.Button5.configure(activeforeground="#000000")
        self.Button5.configure(background="black")
        self.Button5.configure(disabledforeground="#a3a3a3")
        self.Button5.configure(foreground="#000000")
        self.Button5.configure(highlightbackground="#d9d9d9")
        self.Button5.configure(highlightcolor="black")
        self.Button5.configure(pady="0")
        self.Button5.configure(state="disabled")
        self.Button5.configure(text='''foreground''', foreground='white')

        self.Button6 = Button(top, command=self.bground)
        self.Button6.place(relx=0.32, rely=0.88, height=30, width=83)
        self.Button6.configure(activebackground="light slate gray")
        self.Button6.configure(activeforeground="#000000")
        self.Button6.configure(background="black")
        self.Button6.configure(disabledforeground="#a3a3a3")
        self.Button6.configure(foreground="#000000")
        self.Button6.configure(highlightbackground="#d9d9d9")
        self.Button6.configure(highlightcolor="black")
        self.Button6.configure(pady="0")
        self.Button6.configure(state="disabled")
        self.Button6.configure(text='''background''', foreground='white')
            
        
    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y
        self.imag =self.current_image
        

    def on_button_move(self, event):
        x0,y0 = (self.x, self.y) 
        x1,y1 = (event.x,event.y)
        ##print(self.framewidth, self.frameheight)
        y0 = int(y0 -((500 - self.frameheight)/2)) 
        y1 = int(y1-((500 - self.frameheight)/2)) 
        if self.pRect == True:
            rect = ImageDraw.Draw(self.current_image)
            rect.rectangle([x0,y0,x1,y1], fill=None, outline='red')
            
            ##cv2.rectangle(self.currimage, (x0,y0), (x1,y1),[255,0,0], 4)
            
        elif self.value == 2:
            ##cv2.circle(self.current_image,(x1,y1),5,'red',-1)
            cv2.circle(self.mask,(x1,y1),5,0,-1)
            
            circ = ImageDraw.Draw(self.current_image)
            circ.rectangle([x1-5, y1-5, x1+5, y1+5], fill='red')           
            
        elif self.value == 0:
            ##cv2.circle(self.current_image,(x1,y1),5,'blue',-1)
            cv2.circle(self.mask,(x1,y1),5,1,-1)
            
            circ = ImageDraw.Draw(self.current_image)
            circ.rectangle([x1-5, y1-5, x1+5, y1+5], fill='yellow')

        imgtk = ImageTk.PhotoImage(image=self.current_image)
        self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
        self.panel.config(image=imgtk)
        if self.pRect == True:
            self.current_image = self.imag.copy()             

            

    def on_button_release(self, event):
        if self.value != 0 and self.value !=2:
            x0,y0 = (self.x, self.y) 
            x1,y1 = (event.x,event.y)
            y0 = int(y0 -((500 - self.frameheight)/2)) 
            y1 = int(y1-((500 - self.frameheight)/2)) 

            rect = ImageDraw.Draw(self.current_image)
            ##print('rectangle je ',x0,y0,x1,y1)
            rect.rectangle([x0,y0,x1,y1], fill=None, outline='red')
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)
            self.rectangle = (min(x0,x1), min(y0,y1), abs(x1-x0), abs(y1-y0))
            #self.pRect = False

    def fground(self):
        self.value = 0
        print('nastavene je', self.value)

    def bground(self):
        self.value = 2
        print('nastavene je', self.value)
        

    
    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream

        ## if self.index < self.NumberFrames and self.stopped:  # frame captured without any errors
        if ok and self.stopped:  # frame captured without any errors
            frame = imutils.resize(frame, width=self.framewidth,height=self.frameheight)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.currimage = frame
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            self.current = self.current_image
            ##self.current_image= self.current_image.resize([self.framewidth,self.frameheight],PIL.Image.ANTIALIAS)
            
##            self.current_image = cv2.resizeWindow(frame,681,681)
##            frame = self.resizeAndPad(frame, (681,681), 127 )
##            cv2.imshow('frame', frame)
            
            ##imgtk = ImageTk.PhotoImage(image=self.stream[self.index])  # convert image for tkinter
            imgtk = ImageTk.PhotoImage(image=self.current)  # convert image for tkinter
            self.imgtk = imgtk
            #time.sleep(0.2)
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector  
            self.panel.config(image=imgtk)  # show the image
            ##self.index+=1
            #self.root.attributes("-fullscreen",True)
        #self.panel.after(24, self.video_loop)  # call the same function after 30 milliseconds
        self.panel.after(24, self.video_loop)  # call the same function after 30 milliseconds
        
        
    def start(self):
        self.stopped = True
        self.Button3.configure(state="disabled")
        self.Button4.configure(state="normal")
        self.video_loop()
        


    def stop(self):
        self.stopped = False
        self.Button3.configure(state="normal")
        self.Button2.configure(state="normal")
        self.Button4.configure(state="disabled")
        self.Button5.configure(state="normal")
        self.Button6.configure(state="normal")
        print('Button4 - clicked')


    def load(self):
        self.file_path = tkFileDialog.askopenfilename()    
        self.vs = cv2.VideoCapture(self.file_path)
        self.nFrames = int(  self.vs.get(cv2.CAP_PROP_FRAME_COUNT ) )
        self.fps = self.vs.get(cv2.CAP_PROP_FPS )
        self.waitPerFrameInMillisec = int( 1/self.fps * 1000/1 )
        self.framewidth = int(self.vs.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frameheight= int(self.vs.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print('Frames,FPS, WAITFOR',self.nFrames, self.fps, self.waitPerFrameInMillisec)
        print('width and height', self.framewidth, self.frameheight)
        bigger = max(self.framewidth, self.frameheight)
        oneper = bigger/100
        self.percent = float(800/oneper)
        print('percenta',self.percent)
        self.framewidth = int((self.framewidth/100)*self.percent)
        self.frameheight= int((self.frameheight/100)*self.percent)
        print('newwidth and newheight', self.framewidth, self.frameheight)
        self.Button3.configure(state="normal")

        '''load first frame of video or loading of picture'''
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            frame = imutils.resize(frame, width=self.framewidth, height=self.frameheight)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.currimage = frame
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            self.current = self.current_image
            #self.current_image= self.current_image.resize([self.framewidth,self.frameheight],PIL.Image.ANTIALIAS)           
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.imgtk = imgtk
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector  
            self.panel.config(image=imgtk)  # show the image

        self.stream = []
        self.NumberFrames = self.nFrames
        ##self.stream.append(self.current)

        ##while self.NumberFrames > 1:
        ##    ok, frame = self.vs.read()
        ##    frame = imutils.resize(frame, width=self.framewidth, height=self.frameheight)
        ##    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
        ##    self.current_image = Image.fromarray(cv2image)  # convert image for PIL
        ##    self.stream.append(self.current_image)
        ##    self.NumberFrames -=1

        # print('mal by sa prekreslit')
        # imgtk = ImageTk.PhotoImage(image=self.stream[self.nFrames])  # convert image for tkinter
        # self.imgtk = imgtk
        # self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector  
        # self.panel.config(image=imgtk)  # show the image
        ##self.NumberFrames = self.nFrames
        ##self.index = 0

    def grabcut(self):
        img = self.currimage
        #print(mask.shape[:2])
        rect = self.rectangle
        if (self.rect_or_mask == 0):
            self.mask = np.zeros(img.shape[:2],dtype = np.uint8)
            cv2.rectangle(self.mask, (rect[0],rect[1]),(rect[2],rect[3]),[255,0,0], 2)
            bgdmodel = np.zeros((1,65),np.float64)
            fgdmodel = np.zeros((1,65),np.float64)
            #print(bgdmodel, fgdmodel)
            cv2.grabCut(img,self.mask,rect,bgdmodel,fgdmodel,1,cv2.GC_INIT_WITH_RECT)
            #self.mask2 = np.where((self.mask==1)|(self.mask==3),255,0).astype("uint8")
            #img = img* self.mask2[:,:,np.newaxis]
            self.rect_or_mask = 1
            self.pRect = False
       
        elif (self.rect_or_mask == 1):         # grabcut with mask
            bgdmodel = np.zeros((1,65),np.float64)
            fgdmodel = np.zeros((1,65),np.float64)
            #print(bgdmodel, fgdmodel)
            cv2.grabCut(img,self.mask,rect,bgdmodel,fgdmodel,1,cv2.GC_INIT_WITH_MASK)

        mask2 = np.where((self.mask==0) + (self.mask==2),0,1).astype('uint8')
        ##mask2 = np.where((self.mask==0) + (self.mask==2),0,255).astype('uint8')
        img = cv2.bitwise_and(img,img,mask=mask2)
        ##cv2.imshow('output',img)
        ##img = img*mask2[:,:,np.newaxis]

        image = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=image)  # convert image for tkinter
        self.panel2.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector  
        self.panel2.config(image=imgtk)  # show the image
        
        print('Grabcut sa urobil')



if __name__ == '__main__':
    start_gui()


