import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import cv2
import tensorflow as tf
import os
from darkflow.net.build import TFNet
import random as rd
from sklearn.metrics import f1_score

expansion_rate = 2
path_test_data = "../training/"
#path_test_data = "labels/cup/images/"
path_result_folder = "mlp-training/result/"
path_premlp = "mlp-training/result/premlp/"
path_original = "mlp-training/result/original/"
path_cup = "labels/cup/images/"
path_cellphone = "labels/cellphone/images/"
path_paper = "labels/paper/images/"
path_mlp_training = "mlp-training/"


options = {"model": "cfg/truck-yolo.cfg", "load": -1, "gpu":0.75,"threshold":0.9}
#options = {"model": "cfg/truck-yolo.cfg", "load": -1, "gpu":0.0,"threshold":0.9}
#options = {"model": "cfg/truck-yolo.cfg", "load": 56500, "gpu":0.75}
path_yolo_test = "labels/cellphone/images/"

path_mlp_sample_image = "mlp-training/cellphone-0.jpg"
path_mlp_csv = "mlp-training/csv/truck_driver.csv"
path_mlp_model = "mlp-training/saved_models/model-800.ckpt"
size_mlp_data = (100,100)

def relu(num):
    if num > 0:
        return num
    else:
        return 0
    
def expansion(o_img,bbox,rate):
    img = o_img.copy()
    width = bbox[1] - bbox[0]
    height = bbox[3] - bbox[2]
    center = [bbox[0]+width/2,bbox[2]+height/2]
    
    new_bbox = [relu(round(center[0] - (width/2)*rate)), \
                relu(round(center[0] + (width/2)*rate)), \
                relu(round(center[1] - (height/2)*rate)), \
                relu(round(center[1] + (height/2)*rate)) ]
    img = img[new_bbox[2]:new_bbox[3], new_bbox[0]:new_bbox[1]]
    #print(center)
    #print(new_bbox)
    return img

def get_yolo_info(imgcv):
    result = tfnet.return_predict(imgcv)
    if len(result) != 0:
        result = result[0]
        info = {'xmin':result["topleft"]["x"],
                'xmax':result["bottomright"]["x"],
                'ymin':result["topleft"]["y"],
                'ymax':result["bottomright"]["y"],
                'label':result["label"]
               }
        return info
    else:
        return False
    
def pre_mlp(o_img,info,expansion_rate):
    #img = img[info['ymin']:info['ymax'],info['xmin']:info['xmax']]
    img = expansion(o_img, [info['xmin'],info['xmax'], info['ymin'], info['ymax']], expansion_rate)
    #img = expansion(img, [info['xmin'],info['xmax'], img.shape[0]-info['ymax'], img.shape[0]-info['ymin']], expansion_rate)
    return img

def draw(img,info):
    output = img.copy()
    cv2.rectangle(output, (info['xmin'], info['ymin']), (info['xmax'], info['ymax']), (0,0,255),2)
    text_x, text_y = info['xmax']+10 , info['ymin']+10 
    cv2.putText(output, info['label'], (text_x, text_y),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    return output

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


    
img = cv2.imread(path_mlp_sample_image,0)
img2 = cv2.resize(img, size_mlp_data)
img2 = img2.flatten()
#print(img2.shape)

imv_csv = pd.read_csv(path_mlp_csv)
class_y = pd.get_dummies(imv_csv['class'], '').as_matrix()#將label做 one_hot encoding
x_train_list, y_train = imv_csv, class_y #資料切割

tf.reset_default_graph()

#### define placeholder ####
input_data = tf.placeholder(dtype=tf.float32, 
                           shape=[None, img2.shape[0]],
                           name='input_data') #用來接 feature 資料進入 tensorflow 

y_true = tf.placeholder(dtype=tf.float32, 
                        shape=[None, y_train.shape[1]],
                        name='y_true') #用來接 label 資料進入 tensorflow 

#### define variables(weight/bias) ####
x1 = tf.layers.dense(input_data, 256, activation=tf.nn.sigmoid, name='hidden1') #第一層hidden layer
x2 = tf.layers.dense(x1, 128, activation=tf.nn.sigmoid, name='hidden2') #第二層hidden layer
x3 = tf.layers.dense(x2, 64, activation=tf.nn.sigmoid, name='hidden3')#第三層hidden layer
out = tf.layers.dense(x3, y_train.shape[1], name='output')# output layer

y_pred = out

#### calculate loss ####
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_pred))

#### optimize variables ####
opt = tf.train.GradientDescentOptimizer(learning_rate=0.001)
update = opt.minimize(loss)

#### init ####
init = tf.global_variables_initializer()
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4
sess = tf.Session(config=config)
sess.run(init)

#tf.global_variables() ## 檢查 graph 裏的 global variables

'''rerun the graph first:
先回到上面將一開始和graph有關的cell先重新執行一遍，將graph架構先建立起來(這樣讀進來的參數才有對應位置存放)'''

sess = tf.Session()
saver = tf.train.Saver()
saver.restore(sess, path_mlp_model) #到我們剛剛存檔的路徑將檔案叫出來，放入graph中對應的參數位置

tfnet = TFNet(options)

def trucker(d,output_folder):
    # video_path = "../FullVideo/DISK1/"
    # video_list = os.listdir(video_path)
    # print(video_list)
    # print(len(video_list))
   
    
    date = d[-8:]
    
    
    path_video_result_folder = output_folder+"/"+date+"/"
    path_video_result_folder2 = output_folder+"/"+date+"/"+"original/"
    

#     if not os.path.isdir(path_video_premlp):
#         os.makedirs(path_video_premlp)
    if not os.path.isdir(path_video_result_folder):
        os.makedirs(path_video_result_folder)
    if not os.path.isdir(path_video_result_folder2):
        os.makedirs(path_video_result_folder2)

    video_list = []
    for video in os.listdir(d):
        if 'avi' in video:
            video_list.append(video)
    print(video_list)

    total = 0
    count = 0
    switch = 1
    move_list = []
    stop_count = []
    move_count = []
    status_list = []
    stop_rate = 0.8
    start_rate = 0.2
    standard = 0
    vnum = 1
    for video in video_list:
        print('Now processing:', video, vnum,"/",len(video_list))
        vnum+=1
        cap = cv2.VideoCapture(d+"/"+video)
        timeF = 100
        c = 0
        # 以迴圈從影片檔案讀取影格，並顯示出來
        while(cap.isOpened()):
            ret, frame = cap.read()
            if frame is None:
                break





            if(c%timeF==0):
                #print(c)
                #判斷車子是否行進間   
    #             new_img = frame[100:250,350:500]
                new_img = frame[100:250,360:500]
                if c==0:
                    ret,previous = cv2.threshold(new_img,127,255,cv2.THRESH_BINARY)
                else:
                    ret,current = cv2.threshold(new_img,127,255,cv2.THRESH_BINARY)
                    minus = cv2.subtract(current,previous)
                    previous = current.copy()
                    move = np.sum(minus/255)

    #                 cv2.imshow('mytitle',minus)
    #                 #print(move)
    #                 if cv2.waitKey(1) & 0xFF == ord('q'):
    #                     break
    #                 if c== 3000:
    #                     cap.release()
    #                     cv2.destroyAllWindows()

                    if move < 2000:
                        status_list.append(0)
                    else:
                        status_list.append(1)

                    if len(status_list) == 10:
                        if sum(status_list) < 10*(1-stop_rate):
                            switch = 0
                        if sum(status_list) > 10*start_rate:
                            switch = 1
                        #print(status_list, switch)
                        status_list.pop(0)



                #print(type(frame))
                img = frame[:,5:300]
                
                
                if switch == 1:
                    yolo_info = get_yolo_info(img)
                    if yolo_info != False:
                        #print(yolo_info)
                        #yolo = draw(img, yolo_info)
                        #cv2.imwrite(path_video_yolo+str(c)+".jpg", yolo)
                        #cv2.imwrite(path_original+file, draw(img, yolo_info))
                        #expansion process
                        bbox = pre_mlp(img,yolo_info,expansion_rate)
                        #cv2.imwrite(path_video_premlp+video[:video.index('.')]+'_'+str(count)+".jpg", bbox)
                        #print(path_video_premlp+str(count)+".jpg")
                        #preprocess
                        bbox = cv2.resize(bbox,size_mlp_data)
                        bbox = cv2.cvtColor(bbox, cv2.COLOR_BGR2GRAY)
                        #print(bbox.shape)
                        bbox = bbox.flatten()
                        #print(bbox.shape)
                        #tmpx
                        tmpx = np.array([]).reshape((0, img2.shape[0]))
                        tmpx = np.row_stack([tmpx, bbox.flatten()])
                        tmpx /= 255
                        #tmpy
                        tmpy = np.array([]).reshape((0, y_train.shape[1]))
                        tmpy = np.row_stack([tmpy, class_y[0]])
                        tr_pred = sess.run([y_pred], feed_dict={input_data:tmpx})
                        #print('aaaaaa')
                        if tr_pred[0][0][0] > tr_pred[0][0][1]:
                        #if tr_pred[0][0][0] > 0.5:
                            print(tr_pred)
                            img = draw(img, yolo_info)
                            cv2.imwrite(path_video_result_folder+video[:video.index('.')]+'_'+str(count)+".jpg", img)
                            cv2.imwrite(path_video_result_folder2+video[:video.index('.')]+'_'+str(count)+".jpg", frame)
                            print(path_video_result_folder+video[:video.index('.')]+'_'+str(count)+".jpg")
                        count += 1
            c += 1
        print('total count:', count)
        print('----------------------------')
        cap.release()
        cv2.destroyAllWindows()
        #print('Object detected files:',count,'/',total)


