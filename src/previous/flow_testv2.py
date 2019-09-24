
from darkflow.net.build import TFNet
import cv2
import numpy as np
import os


#options = {"model": "cfg/truck-tiny-yolo.cfg", "load": -1, "gpu":0.75}
options = {"model": "cfg/truck-yolo-v2.cfg", "load": -1, "gpu":0.75, "threshold": 0.1}

#options = {"model": "cfg/yolo.cfg", "load": "bin/yolov2.weights", "threshold": 0.1}



tfnet = TFNet(options)
path = 'closebaffle-and-cellphone/images/'

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

for file in os.listdir(path):
    if '.jpg' in file:
        
        imgcv = cv2.imread(path+file)
        imgcv = detect(imgcv)
        if len(imgcv) != 0:
            cv2.imwrite(path+'result/'+file,imgcv)
            

        
