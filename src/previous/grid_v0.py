#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we create a bit
more complicated window layout using
the QGridLayout manager. 

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""



import sys, re, os
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QBasicTimer
from time import sleep
import DNN_truck_driver_test_v2 as td
import time

#Global variable
url_list = []
file_list = []
class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        #Define Properties
        self.setAcceptDrops(True)
        self.setWindowTitle('Trucker Detection')
        self.location = 'NULL'
        self.timer = QBasicTimer()
        self.step = 0
        #self.center()
        


        #Define Objects
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        button2 = QPushButton("Browse", self)
        self.outtext = QLabel("",self)
        #self.hinttext = QLabel("Please drag folders to here.",self)
        self.foldertext = QLabel("",self)
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0,100)
        self.button = QPushButton("Start", self)


        #Layout management
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(button2, 1, 0)
        grid.addWidget(self.outtext, 1, 1)

        #grid.addWidget(self.hinttext, 2,0,2,1)
        grid.addWidget(self.foldertext,2,0,2,1)

        grid.addWidget(self.button,3,0)
        grid.addWidget(self.progressBar,3,1)
        
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 350, 200)
       
        #Action Task
        self.button.clicked.connect(self.onStart)
        button2.clicked.connect(self.browse)

        self.myLongTask = TaskThread(self)
    
        self.myLongTask.notifyProgress.connect(self.onProgress)


    def onStart(self):
        self.myLongTask.start()

    def browse(self):
        global out_folder 
        out_folder = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        self.outtext.setText(out_folder)
         

    def onProgress(self, i):
        if i < 100:
            self.button.setEnabled(False)
        self.progressBar.setValue(i)
    
    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        #initial
        global url_list, file_list
        url_text = ''
        self.location = e.mimeData().urls()

        #dragged folders
        url = re.findall('file:///(.*?)\'',str(self.location))
        url_list += url
        for u in url:
            url_text += u + '\n'
            file_list += os.listdir(u)
                
        content = self.foldertext.text() + url_text
        self.foldertext.setText(content)
        
        print(url_list)
        #tt.trucker(url)
    
    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


class TaskThread(QThread,object):
    notifyProgress = pyqtSignal(int)
  

    def run(self):
        
        #initial
        total = len(url_list)
        count = 0
        #process
        log_name = time.strftime("%Y%m%d-%H%M%S", time.localtime())+'.txt'
        with open(out_folder+'/'+log_name, 'w') as f:
            f.truncate()
            f.close()

        for url in url_list:
            start_time = time.time()
            count += 1
            sleep(1)
            
            
            #load file into model
            td.trucker(url,out_folder)
            end_time = time.time()
            with open(out_folder+'/'+log_name,'a') as f:
                f.write('folder: '+ url + '\n')
                #f.write('video duration:', round(end_time-start_time, 3))
                f.write('start time: ' + time.asctime(time.localtime(start_time)) + '\n')
                f.write('end time: '+ time.asctime(time.localtime(end_time)) + '\n')
                f.write('process duration: ' + str(round(end_time-start_time, 3)) + ' seconds'+ '\n')
                f.write('-----------------------------\n')
                f.write('\n')
                f.close()

            self.notifyProgress.emit(100*count/total)
        
        
        print('start time:', start_time)
        print('end time:', end_time)
        # for file in file_list:
        #     print(file)
        #     count += 1
        #     sleep(1)
        #     #load file into model
       
        #     self.notifyProgress.emit(100*count/total)
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())   