"""
 @author  lijianqing
 @date  2022/12/6 下午10:54
 @version 1.0
"""
import cv2
import os
import shutil
def check_image_size(imgs_path,except_path,h,w,format='jpg'):
    if not os.path.exists(except_path):
        os.makedirs(except_path)
    for i in os.listdir(imgs_path):
        if i.endswith(format):
            img_p = os.path.join(imgs_path,i)
            save_p = os.path.join(except_path,i)
            height, width, channels = cv2.imread(img_p).shape
            if height!=h or width !=w:
                print('img_{}:-------shape:{}:{}:{}:'.format(img_p,height, width, channels))
                shutil.move(img_p,save_p)


check_image_size('/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data_cropped768/val',
                 '/home/lijq/Desktop/data/byd/workspace/data_cropped_merge/data_cropped768/val_r',
                 768,768,'jpg')

def get_imgs_std_mean(imgs_path,format='jpg'):
    import numpy as np
    import os
    import cv2
    for i in os.listdir(imgs_path):
        if i.endswith(format):
            img_path = os.path.join(imgs_path,i)
            image_data = cv2.imread(img_path, -1)
            image_data_mean, image_data_stddev = cv2.meanStdDev(image_data)
            image_data_variance = np.square(image_data_stddev)
            print(image_data_mean)
            print(image_data_stddev)
            print(image_data_variance)

# get_imgs_std_mean('/media/lijq/f373fb19-ec6a-4a1c-96e5-3f2013f3f5c6/RO/split_/pengshang_r/coco_r_ps/val2017')


