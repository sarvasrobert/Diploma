from __future__ import print_function
"""
Sergi Caelles (scaelles@vision.ee.ethz.ch)

This file is part of the OSVOS paper presented in:
    Sergi Caelles, Kevis-Kokitsi Maninis, Jordi Pont-Tuset, Laura Leal-Taixe, Daniel Cremers, Luc Van Gool
    One-Shot Video Object Segmentation
    CVPR 2017
Please consider citing the paper if you use this code.
"""
import os
import sys
#import PIL
from PIL import Image
import numpy as np
#print(sys.version)
import tensorflow as tf
slim = tf.contrib.slim
import matplotlib.pyplot as plt
# Import OSVOS files
root_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(root_folder))
import osvos
from dataset import Dataset
os.chdir(root_folder)

def osvos(filename, masky, iterations):

    ##### imports
    import os
    import sys
    #import PIL
    from PIL import Image
    import numpy as np
    #print(sys.version)
    import tensorflow as tf
    slim = tf.contrib.slim
    import matplotlib.pyplot as plt
    # Import OSVOS files
    root_folder = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.abspath(root_folder))
    import osvos
    from dataset import Dataset
    os.chdir(root_folder)
    ############################
    # User defined parameters
    seq_name = filename
    #realmaskedimage = bwmask + ".jpg"
    #bwmask = bwmask + ".png"
    gpu_id = 0
    train_model = True
    result_path = os.path.join('DAVIS', 'Results', 'Segmentations', '480p', 'OSVOS', seq_name, 'bw_mask')
    print(result_path)

    # Train parameters
    parent_path = os.path.join('models', 'OSVOS_parent', 'OSVOS_parent.ckpt-50000')
    logs_path = os.path.join('models', seq_name)
    max_training_iters = int(iterations)
    #max_training_iters = int(iterations)

    # Define Dataset
    test_frames = sorted(os.listdir(os.path.join('DAVIS', 'JPEGImages', '480p', seq_name)))
    test_imgs = [os.path.join('DAVIS', 'JPEGImages', '480p', seq_name, frame) for frame in test_frames]
    train_imgs = []
    if train_model:
        for image in masky: 
            trainimg = sorted(os.listdir(os.path.join('DAVIS', 'Annotations', '480p', seq_name)))
            train_imgs = [os.path.join('DAVIS', 'JPEGImages', '480p', seq_name, str(image)+".jpg")+' '+
                          os.path.join('DAVIS', 'Annotations', '480p', seq_name, str(image)+".png") for image in masky ]
        dataset = Dataset(train_imgs, test_imgs, './', data_aug=True)
    else:
        dataset = Dataset(None, test_imgs, './')

    # Train the network
    if train_model:
        # More training parameters
        learning_rate = 1e-8
        save_step = max_training_iters
        side_supervision = 3
        display_step = 10
        with tf.Graph().as_default():
            with tf.device('/gpu:' + str(gpu_id)):
                global_step = tf.Variable(0, name='global_step', trainable=False)
                osvos.train_finetune(dataset, parent_path, side_supervision, learning_rate, logs_path, max_training_iters,
                                     save_step, display_step, global_step, iter_mean_grad=1, ckpt_name=seq_name)

    # Test the network
    with tf.Graph().as_default():
        with tf.device('/gpu:' + str(gpu_id)):
            checkpoint_path = os.path.join('models', seq_name, seq_name+'.ckpt-'+str(max_training_iters))
            osvos.test(dataset, checkpoint_path, result_path)

    # Show results
    overlay_color = [255, 0, 0]
    transparency = 0.6
    plt.ion()
    count = 0
    for img_p in test_frames:
        frame_num = img_p.split('.')[0]
        img = np.array(Image.open(os.path.join('DAVIS', 'JPEGImages', '480p', seq_name, img_p)))
        
        if len(frame_num) == 1:
             mask = np.array(Image.open(os.path.join(result_path, '000'+frame_num+'.png')))
        elif len(frame_num) == 2:
             mask = np.array(Image.open(os.path.join(result_path, '00'+frame_num+'.png')))
        elif len(frame_num) == 3:
             mask = np.array(Image.open(os.path.join(result_path, '0'+frame_num+'.png')))
        else:
            mask = np.array(Image.open(os.path.join(result_path, frame_num+'.png')))
        mask = mask//np.max(mask)
        im_over = np.ndarray(img.shape)
        im_over[:, :, 0] = (1 - mask) * img[:, :, 0] + mask * (overlay_color[0]*transparency + (1-transparency)*img[:, :, 0])
        im_over[:, :, 1] = (1 - mask) * img[:, :, 1] + mask * (overlay_color[1]*transparency + (1-transparency)*img[:, :, 1])
        im_over[:, :, 2] = (1 - mask) * img[:, :, 2] + mask * (overlay_color[2]*transparency + (1-transparency)*img[:, :, 2])
        plt.imshow(im_over.astype(np.uint8))
        
        '''if len(frame_num) == 1:
             mask = np.array(Image.open(os.path.join(result_path, '000'+frame_num+'.jpg')))
        elif len(frame_num) == 2:
             mask = np.array(Image.open(os.path.join(result_path, '00'+frame_num+'.jpg')))
        elif len(frame_num) == 3:
             mask = np.array(Image.open(os.path.join(result_path, '0'+frame_num+'.jpg')))
        else:
            mask = np.array(Image.open(os.path.join(result_path, frame_num+'.jpg')))'''
        plt.imsave(os.path.join('DAVIS', 'Results', 'Segmentations', '480p', 'OSVOS', seq_name , frame_num+'.jpg'), im_over.astype(np.uint8))
        plt.axis('off')
        plt.show()
        plt.pause(0.01)
        plt.clf()
        count +=1
