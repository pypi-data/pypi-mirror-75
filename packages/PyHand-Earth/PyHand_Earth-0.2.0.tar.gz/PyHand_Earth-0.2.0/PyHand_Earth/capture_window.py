"""Stand-alone program that uses OpenCV to capture live webcam images
and test TensorFlow model predictions using saved model"""
import os
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from keras.models import load_model
from capture_thread import CaptureThread

# Suppress TensorFlow info and warnings. Errors still displayed.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class QtCapture(QtWidgets.QWidget):

    def __init__(self, earth, desktop, screen, *args, **kwargs):
        super(QtCapture, self).__init__(*args, **kwargs)

        #Old Model Name
        #self.model = load_model('pyearth_cnn_model_200612_1744.h5')
        #self.model = load_model('pyearth_cnn_model_new_test2.h5')
        #self.model = load_model('pyearth_cnn_model_without_nothing.h5')
        #New Model Name
        self.model = load_model('pyearth_cnn_model_0724.h5')
        self.class_names = ['INDEX_UP', 'V_SIGN', 'THUMB_LEFT', 'THUMB_RIGHT', 'FIST', 'FIVE_WIDE',
                            'PALM', 'SHAKA', 'NOTHING']

        self.earth = earth
        self.desktop = desktop
        self.screen = screen

        self.video_frame = QLabel(self)
        self.layout_one = QVBoxLayout()
        self.layout_one.setContentsMargins(0, 0, 0, 0)
        self.layout_one.addWidget(self.video_frame)
        self.setLayout(self.layout_one)

        self.camera = cv2.VideoCapture(-1)

        self.output = ""

        self.cap_thread = None

        self.start_thread()

    def start_thread(self):
        self.cap_thread = CaptureThread(self.earth, self.model, self.class_names, self.camera, self.desktop, self.screen)
        self.cap_thread.updatePixmap.connect(self.setVideoFrame)
        self.cap_thread.updateOutput.connect(self.setOutput)
        self.cap_thread.start()

    def stop_thread(self):
        if self.cap_thread:
            self.cap_thread.stop_thread()

    @pyqtSlot(QPixmap)
    def setVideoFrame(self, frame):
        self.video_frame.setPixmap(frame)

    @pyqtSlot(str)
    def setOutput(self, output):
        self.output = output

    def get_output(self):
        return self.output

    def delete(self):
        self.camera.release()
