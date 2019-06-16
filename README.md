
# Segmentation of motion blurred object in video 

## Diploma thesis - Alpha 1.0 

-Implemented in Python 3.6, OpenCV2 library, Tensorflow, Matplotlib, Scipy.


**Description of developing application:**

*My thesis aim to segment motion blurred object in video.*
* Implement GrabCut method for semi-automatical selection of object.
* OSVOS - One shot video object Segmentation - state of the art in precision(79% for one labeled image, 86% for 3 labeled images). 
* Compare solution of detection of motion blur features & Optical flow solutions & Alpha Matting solutions.  
* Implement one of these solutions and compare with state-of-the-art results.

Links:
-Thesis: https://www.overleaf.com/read/gpyvkzbgdgxk  <br />
-OSVOS (Tensorflow): https://github.com/scaelles/OSVOS-TensorFlow  <br />
-Python 3.6 Download: https://www.python.org/downloads/  <br />
-OpenCV2 & Matplotlib library: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html  <br />

You can find whole application under App folder. 
Application consist of main.py, main_support.py, classifier.py, OSVOS folder, KNN_Matting folder.

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