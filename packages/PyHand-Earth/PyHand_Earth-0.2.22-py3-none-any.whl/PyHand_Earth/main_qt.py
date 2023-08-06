"""
Starts a Qt application that drives input and output from an opencv window to the Google Earth
program
"""
import os
import sys
import time
import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, \
     QPushButton, QWidget, QApplication, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThreadPool, QStateMachine, QState, pyqtSignal

from .keyboard_commands import KeyboardCommands
from .google_earth import GoogleEarth
from .capture_window import QtCapture
from .file_download import FileDownload
from .command_thread import CommandThread

class MainWindow(QMainWindow):
    """
    This is a class that creates a PyQt5 window containing start, stop, and exit buttons as
    well as gesture icons. The window is the main window for our program.

    Attributes:
        commands: Instantiate keyboard command class object for sending commands to Google Earth
        stop_commands (bool) : Flag for enabling and disabling worker thread
        capture: Instantiate QtCapture class when start video button is pressed
        google_earth: GoogleEarth class object
        new_position (int) : X and Y position values of Google Earth window
        window_resize (int) : Width and height of resized Google Earth window
        title_bar_offset (int) : Offset value to account for windowless frame when positioning
            window
        threadpool : Instantiate QThreadpool class
        layout : Instantiate QVBoxLayout or QHBoxLayout classes, used for aligning images and
            buttons
        label_dict (dict) : Contains labels that are used to display gesture icon images
        image_list (list) : Contains names of image files for gesture icon images
        title_list (list) : Contains names of titles for corresponding gesture images
        label : Instantiate QLabel class, labels used to hold gesture icon images and text
        button : Instantiate QPushButton class, buttons used to start, stop, and exit program
        widget : Insantiate QWidget class, contains and displays labels and buttons

    Args:
        earth : GoogleEarth class object

    """
    onSignal = pyqtSignal()
    offSignal = pyqtSignal()

    def __init__(self, earth, desk_geo, screen_geo, *args, **kwargs):
        """
        Please see help(MainWindow) for more info
        """
        super(MainWindow, self).__init__(*args, **kwargs)
        # Instantiate KeyboardCommands class
        self.commands = KeyboardCommands()
        # Flag for stopping commands to GE window
        self.stop_commands = False
        # Will hold hand_recognition QtCapture class
        self.capture = None
        # Will hold camera object for OpenCV
        self.camera = None
        # Will hold thread for issuing GE commands
        self.command_thread = None
        # Make Qt gesture icon window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Get resolution, window size, and offsets for positioning
        self.google_earth = earth
        # Variables for popup windows
        self.popup_window = None
        self.popup_title = ""
        self.popup_text = ""
        # Available desktop and screen geometry
        self.desktop = desk_geo
        self.screen = screen_geo
        # Sets gesture icon window to be 1/4 of available screen space
        self.qt_window_height = self.desktop.height() * 1/4
        # Set geometry of Qt gesture icon window
        # (this window is the parent of all other Qt windows)
        self.setGeometry(QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
            # Width of Qt gesture window based on width of GE window
            QtCore.QSize(self.desktop.width(), int(self.qt_window_height)),
            self.desktop))
        # Create empty worker object
        self.worker_one = None
        # Initialize threadpool object
        self.threadpool = QThreadPool()
        # Create layouts for organizing Qt gesture icon window
        self.layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()

        self.label_dict = dict()
        fileDir = os.path.dirname(os.path.abspath(__file__)) 
        self.image_list = [fileDir+'/images/index_up.png',fileDir+'/images/v_sign.png', fileDir+'/images/thumb_left.png',
                           fileDir+'/images/thumb_right.png', fileDir+'/images/fist.png', fileDir+'/images/five_wide.png',
                           fileDir+'/images/palm.png', fileDir+'/images/shaka.png']
        self.title_list = ['Move Up', 'Move Down', 'Move Left', 'Move Right', 'Zoom In',
                           'Zoom Out', 'Tilt Up', 'Tilt Down']
        # Create and add 6 labels containing hand gesture image to layout2 and 6
        # labels with the gesture descriptions to layout1
        for num in range(0, 8):

            self.label = QLabel(self)
            self.pixmap = QPixmap(self.image_list[num])

            if self.screen.width() >= 2560:
                self.pixmap = self.pixmap.scaledToWidth(225)
            elif self.screen.width() >= 1920:
                self.pixmap = self.pixmap.scaledToWidth(185)
            elif self.screen.width() > 1280 and self.screen.height() >= 1200:
                self.pixmap = self.pixmap.scaledToWidth(175)
            elif self.screen.width() > 800 and self.screen.height() >= 1024:
                self.pixmap = self.pixmap.scaledToWidth(125)
            elif self.screen.width() > 800:
                self.pixmap = self.pixmap.scaledToWidth(100)
            else:
                self.pixmap = self.pixmap.scaledToWidth(50)

            self.label.setPixmap(self.pixmap)

            self.label_title = QLabel(self.title_list[num])

            self.label_dict[num] = self.label

            self.layout2.addWidget(self.label_dict[num], alignment=QtCore.Qt.AlignCenter)

            self.layout1.addWidget(self.label_title, alignment=QtCore.Qt.AlignCenter)

        # Create state machine to reliably handle state changes during threading
        self.state_machine = QStateMachine()
        self.state_button = QPushButton(self)
        self.state_button.setStyleSheet("background-color: silver")
        self.state_button.released.connect(self.check_state)
        self.on = QState()
        self.off = QState()
        self.on.addTransition(self.offSignal, self.off)
        self.on.addTransition(self.state_button.clicked, self.on)
        self.off.addTransition(self.onSignal, self.on)
        self.on.assignProperty(self.state_button, "text", "Start Gesture Navigation")
        self.off.assignProperty(self.state_button, "text", "Stop Gesture Navigation")
        self.state_machine.addState(self.off)
        self.state_machine.addState(self.on)
        self.state_machine.setInitialState(self.on)
        self.state_machine.start()
        # Create gesture tips button and connect it to
        self.tips_button = QPushButton("Gesture Navigation Tips")
        self.tips_button.setStyleSheet("background-color: silver")
        self.tips_button.pressed.connect(self.start_gesture_tips)
        # Create stop button and connect it to stop_opencv function
        self.exit_button = QPushButton("Exit Program")
        self.exit_button.setStyleSheet("background-color: silver")
        self.exit_button.pressed.connect(self.exit)
        # Add start and stop button to layout 3
        self.layout3.addWidget(self.tips_button)
        self.layout3.addWidget(self.state_button)
        self.layout3.addWidget(self.exit_button)
        # Add layout 1, 2, and 3 to layout
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.layout.addLayout(self.layout3)
        # Create widget to hold layout, add layout to widget
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        # Set widget with layouts as central widget
        self.setCentralWidget(self.widget)

    # Function to display pop up windows and block GUI loop until closed
    def show_popup(self, title, message, icon):
        self.popup_window = QMessageBox()
        self.popup_window.setWindowTitle(title)
        self.popup_window.setText(message)
        self.popup_window.setIcon(icon)
        self.popup_window.setStandardButtons(QMessageBox.Ok)
        self.popup_window.exec()

    # Check state of state machine, take actions based on current state
    def check_state(self):
        current_state = self.state_machine.configuration()

        if self.on in current_state:
            self.check_earth_tips()
        elif self.off in current_state:
            self.stop_opencv()

    def start_gesture_tips(self):
        self.popup_title = "Welcome to PyHand Earth!"

        self.popup_text = """\nThis program allows you to navigate the Google Earth Pro desktop application using only your Webcam and eight hand gestures.
                             \n\t       Instructions and Tips 
                             \n\nFor the best experience, please read the instructions below and then close this window: 
                             \n\n1. Position your webcam so that you have a blank, light-colored background behind you. 
                             \n\n2. Position your right hand and desired gesture in front of the webcam so that it fills a good portion of the orange bounding rectangle in the live video window once it opens. 
                             \n\n3. If the prediction is stuck on the wrong gesture, just shake your hand a little and let it reset. 
                             \n\n4. If you remove your hand completely and have a blank background, navigation should halt. 
                             \n\n5. Happy navigating! """

        self.show_popup(self.popup_title, self.popup_text, QMessageBox.Information)


    def check_earth_tips(self):
        if self.google_earth.start_up_tips():
            self.popup_title = "Gesture Navigation Warning Message"
            self.popup_text = "Please make sure the Start-up Tips window is closed before " + \
                              "starting gesture navigation"
            self.show_popup(self.popup_title, self.popup_text, QMessageBox.Warning)
        else:
            self.open_camera()

    def open_camera(self):
        self.camera = cv2.VideoCapture(-1)
        
        if self.camera is None or not self.camera.isOpened():
            self.popup_title = "No Camera Found Warning Message"
            self.popup_text = "No camera has been detected. \n\nPlease connect a camera before " + \
                              "starting gesture navigation.\n"
            self.show_popup(self.popup_title, self.popup_text, QMessageBox.Warning)
        else:
            self.start_opencv()

    def start_opencv(self):
        """
        Slot function for the start button signal. Instantiates Qt opencv window if not created,
        then starts and shows the window. Once the window is opened, starts worker thread to send
        commands to Google Earth.
        """

        self.google_earth.reposition_earth_small()
        # If opencv window not created, create it
        if not self.capture:
            self.create_opencv()
        else:
            self.capture = None
            self.create_opencv()
        # If command thread exists, remove it
        if self.command_thread:
            self.command_thread = None
        # Start command thread for sending commands to GE
        self.command_thread = CommandThread(self.capture, self.commands)
        self.command_thread.start()
        # Show video capture
        self.capture.show()
        # Ensure button in correct state after else statement
        self.offSignal.emit()
        self.tips_button.setEnabled(False)

    def create_opencv(self):
        # Create QtCapture window for rendering opencv window
        self.capture = QtCapture(self.google_earth, self.desktop, self.screen, self.camera)
        self.capture.setParent(self.widget)
        self.capture.setWindowFlags(QtCore.Qt.Tool)
        self.capture.setWindowTitle("OpenCV Recording Window")

        new_height = int((self.desktop.height() * 3/4) - 35)
        half_width = int(self.desktop.width() / 2)

        if self.screen.width() > 1280:
            window_x = int(self.desktop.width() / 2) + (self.screen.width() - self.desktop.width())
            self.capture.setGeometry(window_x, 0, half_width, new_height)
        elif self.screen.width() > 1152:
            new_width = int((self.desktop.width() * 29/64) + 3)
            window_x = int(half_width + (half_width - new_width) +
                           (self.screen.width() - self.desktop.width()))
            self.capture.setGeometry(window_x, 0, new_width, new_height)
        elif self.screen.width() > 1024:
            new_width = int((self.desktop.width() * 25/64))
            window_x = int(half_width + (half_width - new_width) +
                           (self.screen.width() - self.desktop.width()))
            self.capture.setGeometry(window_x, 0, new_width, new_height)
        else:
            new_width = int((self.desktop.width() * 20/64) - 3)
            window_x = int(half_width + (half_width - new_width) +
                           (self.screen.width() - self.desktop.width()))
            self.capture.setGeometry(window_x, 0, new_width, new_height)

    def stop_opencv(self):
        """
        Slot function for stop button signal. Stops Qt timer in opencv loop and sets
        stop_commands to True to kill worker thread.
        """
        # Set flag to kill GE command thread
        self.command_thread.end_thread()
        time.sleep(1)

        # If capture object exists, end thread, release camera, and close window
        if self.capture:
            self.capture.stop_thread()
            time.sleep(1)
            self.capture.delete()
            self.capture.setParent(None)

        self.google_earth.reposition_earth_large()
        self.onSignal.emit()
        self.tips_button.setEnabled(True)

    def exit(self):
        """
        Slot function for exit button signal. Sets stop_commands to True to kill worker
        thread, then calls close_earth to close Google Earth window, and finally terminates
        the QApplication.
        """
        if self.command_thread:
            self.command_thread.end_thread()
            time.sleep(1)

        # Stop threads, close GE, and exit application
        if self.capture:
            self.capture.stop_thread()
            time.sleep(1)

        self.google_earth.close_earth()

        QtCore.QCoreApplication.instance().quit()

def main():
    """
    Main program loop. Instantiates QApplication and downloads machine learning model.
    Then gets desktop resolution, instantiates GoogleEarth class, and starts Google Earth.
    Finally, instantiates the Qt MainWindow and displays the window. After resizing and
    repositioning the window based on monitor resolution, enters Qt application loop.
    """
    # Create QApp
    app = QApplication(sys.argv)

    # Download and install Google Earth
    file_download = FileDownload()
    file_download.get_google_earth()

    # Download .h5 model
    file_download.get_drive_file()

    # Get desktop resolution
    desktop_widget = app.desktop()
    desktop_geometry = desktop_widget.availableGeometry()

    screen_geometry = desktop_widget.screenGeometry()
    #print(desktop_geometry)

    # Start Google Earth
    google_earth = GoogleEarth(desktop_geometry, screen_geometry)
    google_earth.initialize_google_earth()

    # Create Main Window and show it
    window = MainWindow(google_earth, desktop_geometry, screen_geometry)
    window.show()

    x_position = screen_geometry.width() - desktop_geometry.width()
    y_position = desktop_geometry.bottom() - window.height()

    # Gesture window moved to bottom of screen
    window.move(x_position, y_position)

    app.exec_()

if __name__ == '__main__':
    main()
