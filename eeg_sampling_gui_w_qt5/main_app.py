from PyQt5.QtCore import QDir, Qt, QUrl, QTimer,QThreadPool
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, QHBoxLayout, QVBoxLayout,
                            QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QWidget, QAction)
from PyQt5.QtGui import QIcon

from qt_material import apply_stylesheet


import sys
import os

import datetime

from eeg_sampling_worker import EEGDataCollectWorker
from emg_sampling_worker import EMGDataCollectWorkerSignal


class mainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(mainWindow, self).__init__()
        self.setWindowTitle('Test Test')
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()


        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)


        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0,0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)


        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

                # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimeout)



        #Thread 
        self.threadpool = QThreadPool()

        self.worker = EEGDataCollectWorker()
        self.worker.signal.result_sig.connect(self.onDataSampled)
        self.worker.signal.error_sig.connect(self.onError)


        self.cnt = 0
        self.sampled_data = dict()
        self.is_dev_ready = False


    def onTimeout(self):
        pass
        # print(datetime.datetime.now())

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())


    def onError(self, e):
        print(e)

    def onDataSampled(self, result):
        #parse data from tuple
        timestamps = result[0]
        chunks = result[1]

        for t,d in zip(timestamps, chunks):
            #check key redundant
            if str(t) not in self.sampled_data.keys():
                self.sampled_data[str(t)] = d
            else:
                print('found reduntdant at ', str(t))

    def play(self):
        if self.worker.isDeviceReady:
            # play video
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
            else:
                self.mediaPlayer.play()
                self.threadpool.start(self.worker)
        else:
            print("Waiting for device")

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
            print('record at :', datetime.datetime.now())
            self.timer.start(2) #500Hz
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
            self.timer.stop()
            self.export()
            self.worker.is_terminate = True
            self.sampled_data = dict()


    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        # print(position * 500, position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        print("min", duration / 60000.0, "msec", duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
        

    def export(self):
        fname = 'rest1_suguro.txt'
        with open(fname, 'w+') as f:
            for k in self.sampled_data:
                data = ' '.join(str(d) for d in self.sampled_data[k])
                opt = '{} {}'.format(str(k) ,data)
                f.write(opt + '\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme = 'dark_cyan.xml')
    player = mainWindow()
    player.setWindowFlag(Qt.FramelessWindowHint)
    player.resize(640, 480)
    player.showMaximized()
    sys.exit(app.exec_())



    # 103733500
    # 12406536