from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, QTimer, QThreadPool
from pylsl import StreamInlet, resolve_stream
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, QHBoxLayout, QVBoxLayout,
                            QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QWidget, QAction)
from PyQt5 import QtCore
import sys
from qt_material import apply_stylesheet
from datetime import datetime

class DataCollectWorkerSignal(QObject):
    error_sig = pyqtSignal(str)
    result_sig = pyqtSignal(tuple)

class DataCollectWorker(QRunnable):
    def __init__(self):
        super(DataCollectWorker, self).__init__()
        self.signal = DataCollectWorkerSignal()
        self.is_ready = False
        self.createInlet()

        #Status signal for main Task
        self.is_pause = False
        self.is_terminate = False

    def createInlet(self):    
        streams = resolve_stream('type', 'EEG')
        self.inlet = StreamInlet(streams[0])
        self.time_shift_correct = self.inlet.time_correction()
        self.is_ready = True
    
    def isDeviceReady(self):
        return self.is_ready

    def run(self):
        while True:
            if self.is_pause:
                continue
            if self.is_terminate:
                break
            try:
                # sample, timestamp = self.inlet.pull_sample()
                # print(timestamp + self.time_shift_correct, sample)
                chunks, timestamps = self.inlet.pull_chunk()
                # wrap data in dictionary
                
            except Exception as e:
                self.signal.error_sig.emit(str)
            else:
                if timestamps:
                    timestamps = [t + self.time_shift_correct for t in timestamps] #add timeshift correction to each timestamps
                    self.signal.result_sig.emit((timestamps, chunks))
                # pass

    def pause(self):
        self.pause = True

    def terminate(self):
        self.terminate = True

class emptyWindow(QMainWindow):
    def __init__(self, parent = None):
        super(emptyWindow, self).__init__()

        self.setWindowTitle('Test Test')


        self.sc = QWidget()
        self.sc.setStyleSheet("background-color: black")
        self.setCentralWidget(self.sc)
        #Add Horizontal layout
        self.container = QVBoxLayout()
        self.container.setContentsMargins(0,0,0,0)

        self.start_btn = QPushButton('Start Recording Sequece')
        self.start_btn.setEnabled(True)
        # self.start_btn.setStyleSheet('color: white}')
        self.start_btn.setProperty('class', 'danger')
        self.start_btn.resize(150, 50)
        self.start_btn.clicked.connect(self.onStartBtnClicked) 

        self.active_thread_status_btn = QPushButton('Start Recording Sequece')
        self.active_thread_status_btn.setEnabled(True)
        # self.start_btn.setStyleSheet('color: white}')
        self.active_thread_status_btn.setProperty('class', 'warning')
        self.active_thread_status_btn.resize(150, 50)
        self.active_thread_status_btn.clicked.connect(self.onActiveThreadStatusBtnClicked) 

        self.container.addWidget(self.start_btn)
        self.container.addWidget(self.active_thread_status_btn)
        self.sc.setLayout(self.container)


        #time for stop collecting data
        self.timer = QTimer()
        self.timer.setInterval(1000) #every 1s
        self.timer.timeout.connect(self.onIntervalReached)

        self.threadpool = QThreadPool()

        self.cnt = 0
        self.sampled_data = dict()
        self.is_dev_ready = False
    

    def onActiveThreadStatusBtnClicked(self):
        print(self.threadpool.activeThreadCount())

    def onStartBtnClicked(self):
        self.worker = DataCollectWorker()
        self.worker.signal.result_sig.connect(self.onDataSampled)
        self.worker.signal.error_sig.connect(self.onError)
        if self.worker.isDeviceReady:
            self.threadpool.start(self.worker)
            self.timer.start()
        else:
            print("Waiting for device")
    
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

        # self.sampled_data.append(result)
    
    def onError(self, e):
        print(e)

    def onIntervalReached(self):
        t = datetime.now()
        print("Now {}:{}:{} | current data : {}".format(t.hour, t.minute, t.second, len(self.sampled_data)))
        self.cnt+=1
        if(self.cnt == 7):
            self.cnt = 0
            # self.threadpool.stio
            self.worker.is_terminate = True
            self.timer.stop()
            self.sampled_data = dict()
            print("current active thread :", self.threadpool.activeThreadCount())

if __name__ =="__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')
    apply_stylesheet(app, theme = 'dark_cyan.xml')
    m = emptyWindow()
    # m.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    m.resize(800,600)
    # m.showMaximized()
    m.show()
    sys.exit(app.exec_())   
