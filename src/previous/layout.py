from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QBasicTimer
import re,os
from time import sleep
#import Trucker_test as tt
import sys

#Global variable
url_list = []
file_list = []


class MyCustomWidget(QWidget):

    def __init__(self, parent=None):
        super(MyCustomWidget, self).__init__(parent)
             

        #Define Properties
        self.setAcceptDrops(True)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Trucker Detection')
        self.location = 'NULL'
        self.timer = QBasicTimer()
        self.step = 0
        #self.center()
        
        #Define Objects
        self.hinttext = QLabel("Please drag folders to here.",self)
        self.outtext = QLabel("",self)
        self.foldertext = QLabel("",self)
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0,100)
        button = QPushButton("Start", self)
        button2 = QPushButton("Browse", self)

        #Layout Management

        grid = QGridLayout()
        grid.setSpacing(4)

        grid.addWidget(button2, 1, 0)
        grid.addWidget(self.outtext, 1, 1)

        grid.addWidget(self.hinttext, 2, 0)
        grid.addWidget(self.foldertext, 3, 0, 3, 1)

        grid.addWidget(button, 4, 0)
        grid.addWidget(self.progressBar , 4, 0, 4, 1)

        self.setLayout(grid)
        
        # layout = QVBoxLayout(self)

        # layout.addWidget(self.hinttext)
        # layout.addWidget(self.foldertext)
        # layout.addWidget(button)
        # layout.addWidget(self.progressBar)
        
        # self.setLayout(layout)  

        
        #Action Task
        button.clicked.connect(self.onStart)
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
        
        print(file_list)
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
        total = len(file_list)
        count = 0
        #process
        for file in file_list:
            print(file)
            count += 1
            sleep(1)
            #load file into model

            self.notifyProgress.emit(100*count/total)
        # for i in range(101):
        #     if i < 10:
        #         sleep(0.1)
        #     else:
        #         sleep(1)
        #     self.notifyProgress.emit(i)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyCustomWidget()
    #window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())