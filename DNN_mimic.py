import time
import win32api,win32gui,win32con, win32ui
from ctypes import *
import cv2
import sys
import numpy as np
import os
import json
samples = np.loadtxt('number_train/generalsamples.data',np.float32)
responses = np.loadtxt('number_train/generalresponses.data',np.float32)
responses = responses.reshape((responses.size,1))
model = cv2.ml.KNearest_create()
model.train(samples,cv2.ml.ROW_SAMPLE,responses)

VK_CODE = {'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
               'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'F1':0x70,
           'F2':0x71,
           'F3':0x72,
           'F4':0x73,
           'F5':0x74,
           'F6':0x75,
           'F7':0x76,
           'F8':0x77,
           'F9':0x78,
           'F10':0x79,
           'F11':0x7A,
           'F12':0x7B,
           'F13':0x7C,
           'F14':0x7D,
           'F15':0x7E,
           'F16':0x7F,
           'F17':0x80,
           'F18':0x81,
           'F19':0x82,
           'F20':0x83,
           'F21':0x84,
           'F22':0x85,
           'F23':0x86,
           'F24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'left_shift':0xA0,
           'right_shift ':0xA1,
           'left_control':0xA2,
           'right_control':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_Down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'start_mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
'`':0xC0}

#function
def clickLeftCur():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP, 0, 0)
def doubleclickLeftCur():
    clickLeftCur()
    clickLeftCur()

def moveCurPos(x,y):
    windll.user32.SetCursorPos(x, y)

def getCurPos():
    return win32gui.GetCursorPos()

def window_capture(filename):
    hwnd = 0 # 視窗的編號，0號表示當前活躍視窗
    # 根據視窗控制代碼獲取視窗的裝置上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根據視窗的DC獲取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC建立可相容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 建立bigmap準備儲存圖片
    saveBitMap = win32ui.CreateBitmap()
    # 獲取監控器資訊
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[1][2][2]
    h = MoniterDev[1][2][3]
    # print w,h　　　#圖片大小
    # 為bitmap開闢空間
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，將截圖儲存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 擷取從左上角（0，0）長寬為（w，h）的圖片
#     w = 1640
#     h = 289
#     saveDC.BitBlt((260, 572), (w, h), mfcDC, (260, 572), win32con.SRCCOPY)
    saveDC.BitBlt((0,0), (w, h), mfcDC, (0,0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
    
def typeword(word):
    dict = {}
    #處理A~Z
    for w in range(ord('A'), ord('Z') + 1):
        dict[chr(w)] = w
        
    #處理0~9
    for w in range(ord('0'), ord('9') + 1):
        dict[chr(w)] = w
    
    #處理其他
    dict['/'] = 111
    dict['enter'] = 108
    dict[':'] = 0xBA
    for i in word:
        if i == ':':
            win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
            win32api.keybd_event(VK_CODE[';'], 0,0,0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            win32api.keybd_event(VK_CODE[';'],0 ,win32con.KEYEVENTF_KEYUP ,0)
        else:
            win32api.keybd_event(VK_CODE[i],0,0,0)  
        time.sleep(0.2)
    
#開啟程式
button_search = (73,1066)
button_app = (471, 1060)
button_login = (961,659)

moveCurPos(button_app[0],button_app[1])
clickLeftCur()
time.sleep(1)
moveCurPos(button_login[0],button_login[1])
clickLeftCur()
time.sleep(10)

#選取硬碟
button_disk1 = (92,278)

moveCurPos(button_disk1[0],button_disk1[1])
doubleclickLeftCur()
time.sleep(10)
window_capture("haha.jpg")

#選取日期
img = cv2.imread('haha.jpg')
p_origin = (279,648)
ym_origin = (389,601)
box_w = 20
box_h = 20
hor_gap = 46
ver_gap = 35
month_gap = 336
ym_gap = 336
ym_w = 75
ym_h = 20
img[599,269]
count = 0

button_cut = (957,1048)
button_cut_confirm = (620,1042)
button_selectall = (841,548)
button_select2 = (886,495)
button_selectavi = (843,570)
button_starttime = (835, 458)
button_endtime = (1089, 458)
button_browse = (1197, 606)

button_url = (1136, 300)
path_video = 'e:/save/'
button_browse_yes = (1089, 650)
button_cut_yes = (1075, 649)
button_leave = (23, 94)
button_novideo = (959, 603)
tri_origin = (938, 505)
tri_w = 48
tri_h = 40
check_orange = (961, 513)

date_list = []

info = {}
count_video = 0
for i in range(4):
    p_start = (p_origin[0]+i*month_gap,p_origin[1])
    new_ym = (ym_origin[0]+i*ym_gap,ym_origin[1])
    
    if img[new_ym[1],new_ym[0]][0] > 140:
        crop1 = img[new_ym[1]:new_ym[1]+ym_h,new_ym[0]:new_ym[0]+ym_w]
        source1 = crop1
        #判斷年月
        im = source1
        out = np.zeros(im.shape,np.uint8)
        ret,im = cv2.threshold(im,127,255,cv2.THRESH_BINARY_INV)
        #cv2.imshow('123',im)
        cv2.imwrite('number_result/'+str(count)+'.jpg',im)
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
        _,contours,_ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        count = 0
        num_str = 8*['0']
        for cnt in contours:
            #print(cv2.contourArea(cnt))
            if cv2.contourArea(cnt)>0:
                [x,y,w,h] = cv2.boundingRect(cnt)
                #print([x,y,w,h])
                if h>10:
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                    roi = thresh[y:y+h,x:x+w]
                    roismall = cv2.resize(roi,(10,10))
                    roismall = roismall.reshape((1,100))
                    roismall = np.float32(roismall)
                    retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
                    #print('results:',results)
                    string = str(int(results[0][0]))
                    num_str[count] = string
                    #print('num_str:',num_str)
                    count += 1
                    cv2.putText(out,string,(x,y+h),0,1,(0,255,0))
        if num_str[-1] == '0':
            num_str = ['0']+num_str[:-1]
        number = map(int, num_str)
        tmp = []
        for i in num_str:
            tmp.append(i)
        tmp.reverse()
        temp_str = ''
        num_data = temp_str.join(tmp)
        #print(num_data)
        num1 = num_data  
        print('current month:',num1[:-2])
        #print(num1)
        #cv2.imwrite('number_train/number10.png',source1)
        for j in range(6):
            for k in range(7):
                new_pos = (p_start[0]+k*hor_gap,p_start[1]+j*ver_gap)
                #print(new_pos)
                #print(img[new_pos[1],new_pos[0]])
                if img[new_pos[1],new_pos[0]][1] >= 90:
                    crop2 = img[new_pos[1]:new_pos[1]+box_h,new_pos[0]:new_pos[0]+box_w]
                    source2 = crop2
                    #cv2.imwrite('number_train/number11.png',source2)
                    #判斷日期
                    im = source2
                    out = np.zeros(im.shape,np.uint8)
                    ret,im = cv2.threshold(im,127,255,cv2.THRESH_BINARY_INV)
                    #cv2.imshow('123',im)
                    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
                    _,contours,_ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
                    count = 0
                    num_str = 8*['0']
                    taboo = []
                    for cnt in contours:
                        #print(cv2.contourArea(cnt))
                        if cv2.contourArea(cnt)>0:
                            [x,y,w,h] = cv2.boundingRect(cnt)
                            #print([x,y,w,h])
                            if h>6:
                                if [x,y,w,h] not in taboo:
                                    taboo.append([x,y,w,h])
                                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                                    roi = thresh[y:y+h,x:x+w]
                                    roismall = cv2.resize(roi,(10,10))
                                    roismall = roismall.reshape((1,100))
                                    roismall = np.float32(roismall)
                                    retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
                                    string = str(int(results[0][0]))
                                    num_str[count] = string
                                    count += 1
                                    cv2.putText(out,string,(x,y+h),0,1,(0,255,0))
                    number = map(int, num_str)
                    # cv2.imshow('im',im)
                    # cv2.imshow('out',out)
                    tmp = []
                    for i in num_str:
                        tmp.append(i)
                    tmp.reverse()
                    temp_str = ''
                    num_data = temp_str.join(tmp)
                    #print(num_data)
                    num2 = num_data
                    # cv2.waitKey(0)
                    num = num1[:-2]+num2[-2:]
                    date_list.append(num)
                    print(num)
                    info[num] = new_pos
with open(path_video+'ignore.json','r') as f:
    ignore = json.loads(f.read())
    f.close()
    
with open(path_video+'info.json','w') as f:
    f.write(json.dumps(info))
    f.close()
count = 0
for date in info.keys():
    if date not in ignore.keys():
        directory = path_video+date+'/'
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' + directory)



        new_pos = info[date]
        print('Now Capturing',date)
        #點擊該日期    
        moveCurPos(new_pos[0],new_pos[1])
        doubleclickLeftCur()
        time.sleep(20)


        window_capture("check.jpg")
        check = cv2.imread('check.jpg')
        #check = check[tri_origin[1]:tri_origin[1]+tri_h,tri_origin[0]:tri_origin[0]+tri_w]
        if check[check_orange[1],check_orange[0]][2] > 200:
            moveCurPos(button_novideo[0],button_novideo[1])
            clickLeftCur()
            time.sleep(0.5)

            moveCurPos(button_leave[0],button_leave[1])
            clickLeftCur()
            time.sleep(1)
        else:
            #開剪
            moveCurPos(button_cut[0],button_cut[1])
            clickLeftCur()
            time.sleep(0.5)

            moveCurPos(button_cut_confirm[0],button_cut_confirm[1])
            clickLeftCur()
            time.sleep(1)
            moveCurPos(button_selectall[0],button_selectall[1])
            clickLeftCur()
            time.sleep(1)

            moveCurPos(button_select2[0],button_select2[1])
            clickLeftCur()
            time.sleep(1)

            moveCurPos(button_selectavi[0],button_selectavi[1])
            clickLeftCur()
            time.sleep(1)


            #enter time
            #print(count_video)
            if count_video == 0:
                win32api.keybd_event(VK_CODE['left_shift'], 0,0,0)
                win32api.keybd_event(VK_CODE['left_shift'],0 ,win32con.KEYEVENTF_KEYUP ,0)
            moveCurPos(button_starttime[0],button_starttime[1])
            clickLeftCur()
            time.sleep(0.5)
            typeword('000000')

            moveCurPos(button_endtime[0],button_endtime[1])
            clickLeftCur()
            time.sleep(0.5)
            typeword('235959')

            moveCurPos(button_browse[0],button_browse[1])
            clickLeftCur()
            time.sleep(1)

            moveCurPos(button_url[0],button_url[1])
            clickLeftCur()
            time.sleep(1)



            typeword(directory)
            typeword(['enter'])
#             time.sleep(1)
#             typeword(['enter'])

            moveCurPos(button_browse_yes[0],button_browse_yes[1])
            print('press browse yes button')
            clickLeftCur()
            time.sleep(1)

            moveCurPos(button_cut_yes[0],button_cut_yes[1])
            clickLeftCur()
            time.sleep(1)

            moveCurPos(button_leave[0],button_leave[1])
            clickLeftCur()
            time.sleep(1)
            count+=1
            count_video += 1
            if count % 10 ==0:
                time.sleep(300)
                
                        
                        
