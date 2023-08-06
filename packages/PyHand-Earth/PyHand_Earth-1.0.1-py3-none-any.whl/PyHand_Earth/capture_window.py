"""
Implements QtCapture class for displaying OpenCV frames.
"""
import os
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from keras.models import load_model
from .capture_thread import CaptureThread

# Suppress TensorFlow info and warnings. Errors still displayed.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class QtCapture(QtWidgets.QWidget):
    """
    This class creates a window for OpenCV frames to be rendered in.

    Attributes:
        model : Machine learning model object
        class_names (list) : Contains names of gestures
        desktop : Available screen geometry based on current resolution
        screen : Total screen geometry based on current resolution
        video_frame : Instantiates QLabel class, will hold QPixmap that displays current OpenCV
            frame
        camera : OpenCV camera object
        output (string) : Current gesture navigation output
        cap_thread : CaptureThread object, thread used to render OpenCV frames and output recognized
            hand gesture

    Args:
        desktop : Available screen geometry
        screen : Total screen geometry
        camera : OpenCV camera object
    """

    def __init__(self, earth, desktop, screen, camera, *args, **kwargs):
        """
        Please see help(QtCapture) for more info.
        """
        super(QtCapture, self).__init__(*args, **kwargs)
        fileDir = os.path.dirname(os.path.abspath(__file__))
        # Loads machine learning model
        self.model = load_model(fileDir+'/pyearth_cnn_model_0724.h5')
        # List containing all gesture navigation class names
        self.class_names = ['INDEX_UP', 'V_SIGN', 'THUMB_LEFT', 'THUMB_RIGHT', 'FIST', 'FIVE_WIDE',
                            'PALM', 'SHAKA', 'NOTHING']

        self.earth = earth
        # Available screen geometry
        self.desktop = desktop
        # Total screen geometry
        self.screen = screen
        # QLabel that will hold QPixmap for rendering current OpenCV frame
        self.video_frame = QLabel(self)
        # Sets layout of QLabel to take up full QtCapture window
        self.layout_one = QVBoxLayout()
        self.layout_one.setContentsMargins(0, 0, 0, 0)
        # Adds label to layout
        self.layout_one.addWidget(self.video_frame)
        # Adds label layout to window layout
        self.setLayout(self.layout_one)
        # OpenCV camera object
        self.camera = camera
        # Current gesture navigation output
        self.output = ""
        # Will hold CaptureThread object
        self.cap_thread = None
        # Calls start_thread to begin rendering OpenCV frames
        self.start_thread()

    def start_thread(self):
         """
        Starts thread to render OpenCV frames to the QtCapture window and output current gestures.
        """
        # Instantiates CaptureThread class
        self.cap_thread = CaptureThread(self.earth, self.model, self.class_names, self.camera, self.desktop, self.screen)
        # Connect updatePixmap signal to set_video_frame slot
        self.cap_thread.updatePixmap.connect(self.setVideoFrame)
        # Connect updateOutput signal to set_output slot
        self.cap_thread.updateOutput.connect(self.setOutput)
        # Start capture thread
        self.cap_thread.start()

    def stop_thread(self):
        """
        Stops the capture thread if it is currently running.
        """
        # Checks if the capture thread is running, if running calls stop_thread to end it
        if self.cap_thread:
            self.cap_thread.stop_thread()

    @pyqtSlot(QPixmap)
    def setVideoFrame(self, frame):
        """
        Slot for updatePixmap signal. Sets the QtCapture window QLabel to hold the current OpenCV
        frame.

        Parameters:
            frame : QPixmap containing the current OpenCV frame
        """
        self.video_frame.setPixmap(frame)

    @pyqtSlot(str)
    def setOutput(self, output):
        """
        Slot for updateOutput signal. Sets the QtCapture window output to the current navigation
        gesture output.

        Paramaters:
            output (string) : Current gesture navigation output
        """
        self.output = output

    def get_output(self):
        """
        Returns the current gesture navigation output.

        Returns:
            output (string) : Current gesture navigation output
        """
        return self.output

    def delete(self):
        """
        Releases camera object so it can be reused.
        """
        self.camera.release()
