import sys, re, os
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication, QTabWidget)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QBasicTimer
from time import sleep
#import DNN_truck_driver_test_v2 as td
import time
#Global variable
url_list = []
file_list = []

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Trucker Detection')
        self.setGeometry(300, 300, 650, 600)
        self.setAcceptDrops(True)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        
    
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        
        self.setAcceptDrops(True)
        self.location = 'NULL'
        self.timer = QBasicTimer()
        self.step = 0

        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Cellphone")
        self.tabs.addTab(self.tab2,"Baffle")
        
        # Create first tab
    

            #Define Objects
        hint = QLabel("請輸入車號：",self)
        car_number = QLineEdit(self)
        browse_button_cellphone = QPushButton("Browse", self)
        self.outtext_cellphone = QLabel("",self)
        #self.hinttext = QLabel("Please drag folders to here.",self)
        self.foldertext_cellphone = QLabel("",self)
        self.progressBar_cellphone = QProgressBar(self)
        self.progressBar_cellphone.setRange(0,100)
        self.start_button_cellphone = QPushButton("Start", self)
        grid_cellphone = QGridLayout()
        #grid.setSpacing(10)
        grid_cellphone.addWidget(hint, 0, 0)
        grid_cellphone.addWidget(car_number, 0, 1)
        grid_cellphone.addWidget(browse_button_cellphone, 1, 0)
        grid_cellphone.addWidget(self.outtext_cellphone, 1, 1)
        grid_cellphone.addWidget(self.foldertext_cellphone,2,1)
        grid_cellphone.addWidget(self.start_button_cellphone,3,0)
        grid_cellphone.addWidget(self.progressBar_cellphone,3,1)
        
        self.tab1.setLayout(grid_cellphone)

        # Create second tab
    

            #Define Objects
        browse_button_baffle = QPushButton("Browse", self)
        self.outtext_baffle = QLabel("",self)
        #self.hinttext = QLabel("Please drag folders to here.",self)
        self.foldertext_baffle = QLabel("",self)
        self.progressBar_baffle = QProgressBar(self)
        self.progressBar_baffle.setRange(0,100)
        self.start_button_baffle = QPushButton("Start", self)
        grid_baffle = QGridLayout()
        #grid.setSpacing(10)
        grid_baffle.addWidget(browse_button_baffle, 1, 0)
        grid_baffle.addWidget(self.outtext_baffle, 1, 1)
        grid_baffle.addWidget(self.foldertext_baffle,2,0,2,1)
        grid_baffle.addWidget(self.start_button_baffle,3,0)
        grid_baffle.addWidget(self.progressBar_baffle,3,1)
        
        self.tab2.setLayout(grid_baffle)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        #Action Task
        self.start_button_cellphone.clicked.connect(self.onStart)
        browse_button_cellphone.clicked.connect(self.browse)

        self.myLongTask = TaskThread(self)
    
        self.myLongTask.notifyProgress.connect(self.onProgress)
        
    def onStart(self):
        self.myLongTask.start()

    def browse(self):
        global out_folder 
        out_folder = QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        self.outtext_cellphone.setText(out_folder)
         

    def onProgress(self, i):
        if i < 100:
            self.start_button_cellphone.setEnabled(False)
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
                
        content = self.foldertext_cellphone.text() + url_text
        self.foldertext_cellphone.setText(content)
        
        print(url_list)
        #tt.trucker(url)
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
            #td.trucker(url,out_folder)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())