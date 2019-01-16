
# Detection of motion blurred object in video 

## Diploma thesis - Alpha 0.5 

-Implemented in Python 3.6 and OpenCV2 library.


**Description:**

*My thesis aim to detect motion blurred object in video.*
* First step of program is to automaticaly select object of interest by Grabcut method.
* Second Step is OSVOS - One shot video object segmentation - state of the art precision is  79% for this topic. 
* Third step is to create Bounding box around segmented mask and detect if any motion blur is created
* Fourth step is segment motion blur with highest possible precision  

Links:
Thesis: https://www.overleaf.com/read/gpyvkzbgdgxk

**Screens:**

![GUI of application](https://github.com/sarvasrobert/Diploma/blob/master/a.png?raw=true)

![GrabCut 1st object extraction step - setting rectangle](https://github.com/sarvasrobert/Diploma/blob/master/b.png?raw=true)

Outputs and testing of OSVOS object segmentation from video based on 1 labeled frame.
1.Dog 100 iterations, res:800x450px
![OSVOS - dog 100 iterations](https://github.com/sarvasrobert/Diploma/blob/master/dog_100.gif?raw=true)
2.Dog 100 iterations, res:800x450px
![OSVOS - dog2 100 iterations](https://github.com/sarvasrobert/Diploma/blob/master/dog2_100.gif?raw=true)
3.Man 100 iterations, res:800x450px
![OSVOS - human 100 iterations](https://github.com/sarvasrobert/Diploma/blob/master/soko_100.gif?raw=true)