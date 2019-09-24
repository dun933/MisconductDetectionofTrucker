
from darkflow.net.build import TFNet
import cv2
import numpy as np
import os
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

#options = {"model": "cfg/truck-tiny-yolo.cfg", "load": -1, "gpu":0.75}
options = {"model": "cfg/truck-yolo.cfg", "load": -1, "gpu":0.75}

#options = {"model": "cfg/yolo.cfg", "load": "bin/yolov2.weights", "threshold": 0.1}

tfnet = TFNet(options)
path = "../yolo_truck_driver/images/"
path2 = "../training/"
total = 0
count = 0
count_ab = 0
count_nor = 0
total_ab = 0
total_nor = 0
imgcv = cv2.imread(path+'1.jpg')
result = tfnet.return_predict(imgcv)
print(result)
# for file in os.listdir(path2):
#     total += 1
#     if '.jpg' in file:
#         #print(path+file)
#         imgcv = cv2.imread(path2+file)
#         imgcv = detect(imgcv)
#         if len(imgcv) != 0:
#             count += 1
#             cv2.imwrite('../Result/'+file,imgcv)
#             if 'ab' in file:
#                 count_ab+=1
#             else:
#                 count_nor+=1

#         print('Object detected files:',count,'/',total)
# print(count_ab, count_nor)

# for i in range(25):
#     cap = cv2.VideoCapture('../完整影片/20180628/'+str(i)+'.avi')
#     timeF = 10
#     c = 0
#     # 以迴圈從影片檔案讀取影格，並顯示出來
#     while(cap.isOpened()):
#         ret, frame = cap.read()
#         if frame is None:
#             break

#         if(c%timeF==0):
#             #print(type(frame))
#             imgcv = detect(frame)
#             if len(imgcv) != 0:
#                 count += 1
#                 cv2.imwrite('../Result/'+str(count)+'.jpg',imgcv)
#                 # cv2.imshow('Test',imgcv)
#                 # if cv2.waitKey(1) & 0xFF == ord('q'):
#                 #     break
#             total += 1
#         c += 1
#     cap.release()
#     cv2.destroyAllWindows()
#     print('Object detected files:',count,'/',total)
        