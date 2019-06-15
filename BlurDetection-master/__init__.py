#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Will Brennan'

# built-in modules
# Standard modules
# Custom modules

from main import *
from FocusMask import *
import scripts

import locale
locale.getdefaultlocale()


import os
import cv2
import numpy
##import BlurDetection

img_path = input("type img path here ")
assert os.path.exists(img_path), "img_path does not exists"
img = cv2.imread(img_path, encoding=locale.getdefaultlocale()[1])
img_fft, val, blurry = blur_detector(img)
print ("this image {0} blurry".format(["isn't", "is"][blurry]))
msk, val = blur_mask(img)
display('img', img)
display('msk', msk)
cv2.waitKey(0)