
# Detection of motion blurred object in video 

## Diploma thesis - Alpha 0.5 

-Implemented in Python 3.6, OpenCV2 library, Tensorflow.


**Description:**

*My thesis aim to detect motion blurred object in video.*
* Implement GrabCut method for semi-automatical selection of object.
* OSVOS - One shot video object Segmentation - state of the art in precision(79% for one labeled image, 86% for 3 labeled images). 
* Create tracking of object and delete all unwanted patches of objects mask.
* Study motion blur - Confront Pattern recognition solutions with other solutions and implement the best solution 

Links:
-Thesis: https://www.overleaf.com/read/gpyvkzbgdgxk
-OSVOS (Tensorflow): https://github.com/scaelles/OSVOS-TensorFlow
-Python 3.6 Download: https://www.python.org/downloads/
-OpenCV2 & Matplotlib library: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html

**Screens:**

![GUI of application](https://github.com/sarvasrobert/Diploma/blob/master/a.png?raw=true)

![GrabCut 1st object extraction step - setting rectangle](https://github.com/sarvasrobert/Diploma/blob/master/b.png?raw=true)

**Outputs and testing of OSVOS object segmentation from video based on 1 labeled frame.**

1.Dog 100 iterations, res:800x450px
![OSVOS - dog 100 iterations](https://github.com/sarvasrobert/Diploma/blob/master/dog_100.gif?raw=true)

2.Dog 100 iterations, res:800x450px
![OSVOS - dog2 100 iterations](https://github.com/sarvasrobert/Diploma/blob/master/dog2_100.gif?raw=true)

3.Man 100 iterations, res:800x450px
![OSVOS - human 100 iterations](https://github.com/sarvasrobert/Diploma/blob/master/soko_100.gif?raw=true)