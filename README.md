
# Detection of motion blurred object in video 

## Diploma thesis - Alpha 0.1 

Implemented in Python 3.6 and OpenCV2 library.
** Description: **
* My thesis aim to detect motion blurred object in video.
* First step of program is to automaticaly select object of interest by Grabcut method.
* Second Step is OSVOS - One shot video object segmentation - state of the art precision is  79% for this topic. 
* Third step is to create Bounding box around segmented mask and detect if any motion blur is created
* Fourth step is segment motion blur with highest possible precision  


**Screens:**

![GUI of application](https://github.com/sarvasrobert/Diploma/blob/master/a.png?raw=true)

![GrabCut 1st object extraction step - setting rectangle](https://github.com/sarvasrobert/Diploma/blob/master/b.png?raw=true)
	
![GrabCut 2st object extraction step - labeling image with FG/BG](https://github.com/sarvasrobert/Diploma/blob/master/c.png?raw=true)