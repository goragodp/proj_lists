from random import sample
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QDir, Qt, QUrl, QThread, QTimer, QEventLoop
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QDialog, QMainWindow, QApplication, QFileDialog, QHBoxLayout, QVBoxLayout,
                            QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QWidget, QAction)
from PyQt5.QtGui import QIcon

from qt_material import apply_stylesheet
import datetime

import sys
import os
import datetime

class StartPage(QDialog):
    def __init__(self, widget, parent = None):
        super(StartPage, self).__init__(parent)

        self.widget = widget

        self.label = QLabel('Ready')
        self.label.setAlignment(Qt.AlignCenter)
        self.btn = QPushButton('Start Recording')
        # self.btn.setProperty('class', 'big_button')
        self.btn.clicked.connect(self.onBtnClicked)

        self.setStyleSheet("background-color: black")
        # self.setCentralWidget(self.sc)
        #Add Horizontal layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,10,0)

        self.layout.setSpacing(30)
        self.layout.addStretch()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.btn)
        self.layout.addStretch()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

    def onBtnClicked(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

class CuePage(QDialog):
    def __init__(self, widget, parent = None):
        super(CuePage, self).__init__(parent)

        self.widget = widget

        self.cue_img = QLabel()
        self.cue_img.setPixmap(QtGui.QPixmap('assets/cue.png'))
        self.cue_img.setAlignment(Qt.AlignCenter)
        self.cue_img.show()


        self.setStyleSheet("background-color: black")

        #Add Horizontal layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)

        self.btn = QPushButton('Go to next page')
        self.btn.clicked.connect(self.onBtnClicked)

        self.layout.addStretch()
        self.layout.addWidget(self.cue_img)
        self.layout.addStretch()
        self.layout.addWidget(self.btn)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

    def onBtnClicked(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
    
    def playBeep(self):
        import winsound
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)

class ActionObsvVideo(QDialog):
    def __init__(self,widget,  parent = None):
        super(ActionObsvVideo, self).__init__(parent)

        self.widget = widget
        self.label = QLabel('This is label of AO screen')
        self.btn = QPushButton('Go to next page')
        self.btn.clicked.connect(self.onBtnClicked)
        

        self.action_obersve_video = QVideoWidget()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.action_obersve_video)
        self.media_player.setMedia(QMediaContent(QUrl('assets/IMG_2659.MOV')))
        self.action_obersve_video.resize(1024, 768)
        self.media_player.stateChanged.connect(self.mediaStateChanged)
        self.media_player.setMuted(True)
        self.media_player.play()

        self.setStyleSheet("background-color: black")
        # self.setCentralWidget(self.sc)
        #Add Horizontal layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.action_obersve_video)
        self.layout.addStretch()
        self.layout.addWidget(self.btn)

        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)


        self.is_done_playing = False

        
    def getVideoPlayState(self):
        return self.media_player.state()
    
    def mediaStateChanged(self, state):
        if self.media_player.state() == QMediaPlayer.State.StoppedState or self.media_player.state() == QMediaPlayer.State.PausedState :
            self.is_done_playing = True
        else:
            self.is_done_playing = False

    def onBtnClicked(self):
        if self.media_player.state() == QMediaPlayer.State.PlayingState: #Playing
            self.media_player.pause()
        
        self.widget.setCurrentIndex(self.widget.currentIndex() +1)
    

class ActionExecPage(QDialog):
    def __init__(self, widget, parent = None):
        super(ActionExecPage, self).__init__(parent)

        self.widget = widget

        self.btn = QPushButton('return')
        self.btn.clicked.connect(self.onBtnClicked)
        self.setStyleSheet("background-color: black")
        #Add Horizontal layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)

        self.layout.addWidget(self.btn)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

    def onBtnClicked(self):
            self.widget.setCurrentIndex(self.widget.currentIndex() - 4)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Python Record Page')
        self.widget = QtWidgets.QStackedWidget()
        self.start_screen = StartPage(self.widget)
        self.cue_screen_ao = CuePage(self.widget)
        self.ao_screen = ActionObsvVideo(self.widget)
        self.cue_screen_ae = CuePage(self.widget)
        self.ae_screen = ActionExecPage(self.widget)


        self.start_widget = QWidget()
        self.label = QLabel('Ready')
        self.label.setAlignment(Qt.AlignCenter)
        self.btn = QPushButton('Start Recording')
        # self.btn.setProperty('class', 'big_button')
        self.btn.clicked.connect(self.onBtnClicked)

        self.setStyleSheet("background-color: black")
        # self.setCentralWidget(self.sc)
        #Add Horizontal layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,10,0)

        self.layout.setSpacing(30)
        self.layout.addStretch()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.btn)
        self.layout.addStretch()
        self.layout.setAlignment(Qt.AlignCenter)
        self.start_widget.setLayout(self.layout)

        self.widget.addWidget(self.start_widget)
        self.widget.addWidget(self.cue_screen_ao)
        self.widget.addWidget(self.ao_screen)
        self.widget.addWidget(self.cue_screen_ae)
        self.widget.addWidget(self.ae_screen)

        self.setCentralWidget(self.widget)
         
        self.current_time = 0
        self.interval_timer = QTimer()
        self.interval_timer.timeout.connect(self.shiftDisplay)
    
    
    def onBtnClicked(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        # self.interval_timer.start(1000)
    
    def shiftDisplay(self):
        self.current_time += 1
    
        # if self.ao_screen.getVideoPlayState == False:
        #     if self.current_time  == 2: #Cue
        #         self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        #     if self.current_time == 4: #AO
        #         self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        # else:
        #     self.interval_timer.stop()

'''
Timeline
Screen :   START  ->   CUE   ->    AO    -> CUE + AudioInvoke   ->     REC    -> DONE  ->   START ....
Time   :   0______2___________4___________8_____________________10______15________16__________17s ....
'''

if __name__ == "__main__":

    app = QApplication(sys.argv)
    apply_stylesheet(app, theme = 'dark_cyan.xml')

    mainWindow = MainWindow()
    mainWindow.resize(800,600)
    mainWindow.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass


    