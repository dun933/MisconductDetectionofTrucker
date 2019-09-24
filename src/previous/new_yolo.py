from darkflow.net.build import TFNet
import os, random, cv2
from shutil import copyfile

def clearfile(path):
    for file in os.listdir(path):
        os.remove(path+file)

#Parameter setting
path_target_anno_folder = "labels/cellphone/annotation/"
path_target_folder = "labels/cellphone/images/"
path_train_folder = "labels/cellphone/train/"
path_test_folder = "labels/cellphone/test/"
path_train_anno_folder = "labels/cellphone/train_anno/"
split_rate = 0.8

#Data split
clearfile(path_train_folder)
clearfile(path_test_folder)
clearfile(path_train_anno_folder)

image_list = os.listdir(path_target_folder)
image_num = len(image_list)

while len(image_list) >= image_num*split_rate:
    file = image_list.pop(random.randint(0,len(image_list)-1))
    copyfile(path_target_folder+file, path_test_folder+file)

for file in image_list:
    copyfile(path_target_folder+file, path_train_folder+file)
    copyfile(path_target_anno_folder+file[:file.index('.')]+'.xml', path_train_anno_folder+file[:file.index('.')]+'.xml')

options = { "model": "cfg/truck-yolo.cfg", \
            "train": True,\
            "dataset":path_target_folder, \
            "annotation":path_train_anno_folder, \
            "gpu":1, \
            "epoch":1500}


tfnet = TFNet(options)
tfnet.train()
