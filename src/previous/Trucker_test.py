#IMPORT SECTION
#%matplotlib inline
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import cv2
import tensorflow as tf
import os
from darkflow.net.build import TFNet
import random as rd
from sklearn.utils import shuffle
options = {"model": "cfg/truck-yolo.cfg", "load": -1, "gpu":0.75}
tfnet = TFNet(options)

#FUNCTION
def detect(imgcv):
    result = tfnet.return_predict(imgcv)
    #print(type(result[0]["topleft"]["x"]))
    if len(result) != 0:
        result = result[0]
        cv2.rectangle(imgcv, 
            (result["topleft"]["x"], result["topleft"]["y"]), 
            (result["bottomright"]["x"], 
            result["bottomright"]["y"]), 
            (0, 255, 0), 4)
        text_x, text_y = result["topleft"]["x"] - 10, result["topleft"]["y"] - 10
        cv2.putText(imgcv, result["label"], (text_x, text_y),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        #print(result)
        # cv2.imshow('Test',imgcv)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return imgcv
    else:
        return np.array([])

def trucker(path,output_folder):

    #VIDEO YOLO
    #file_list = os.listdir(path)
    total = 0
    count = 0
    #print(file_list)
    for f in range(1):
        #cap = cv2.VideoCapture('../完整影片/20180627/'+str(i)+'.avi')
        # cap = cv2.VideoCapture(path+f)
        cap = cv2.VideoCapture(path)
        #print(path+f)
        timeF = 20
        c = 0
        # 以迴圈從影片檔案讀取影格，並顯示出來
        while(cap.isOpened()):
            ret, frame = cap.read()
            if frame is None:
                break

            if(c%timeF==0):
                #print(type(frame))
                origin = frame
                origin = origin[35:,100:300]
    #             cv2.imshow('123',origin)
    #             if cv2.waitKey(1) & 0xFF == ord('q'):
    #                 break
                imgcv = detect(origin)
                if len(imgcv) != 0:
                    count += 1
                    cv2.imwrite('../Output/'+ output_folder + '/' + output_folder + str(count)+'.jpg',imgcv)
                total += 1
            c += 1
        cap.release()
        cv2.destroyAllWindows()
        print('Object detected files:',count,'/',total)
