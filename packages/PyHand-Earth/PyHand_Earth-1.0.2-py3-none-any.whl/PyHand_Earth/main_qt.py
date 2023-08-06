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
        commands: KeyboardCommand class object
        capture: QtCapture class object
        camera: OpenCV camera object
        command_thread: CommandThread class object
        google_earth: GoogleEarth class object
        popup_window: QMessageBox object
        popup_title (string) : Pop up window title
        popup_text (string) : Pop up window body text
        desktop : Available screen geometry based on current screen resolution
        screen : Total screen geometry based on current screen resolution
        qt_window_height (int) : Calculated value for gesture icon window size
        layout : Instantiate QVBoxLayout or QHBoxLayout classes, used for aligning images and
            buttons
        label_dict (dict) : Contains labels that are used to display gesture icon images
        image_list (list) : Contains names of image files for gesture icon images
        title_list (list) : Contains names of titles for corresponding gesture images
        state_machine: Instantiate QStateMachine class, used to control state of program buttons
        label : Instantiate QLabel class, labels used to hold gesture icon images and text
        button : Instantiate QPushButton class, buttons used to start, stop, and exit program
        widget : Insantiate QWidget class, contains and displays labels and buttons

    Args:
        earth : GoogleEarth class object
        desk_geo: Available screen geometry
        screen_geo: Total screen geometry
    """
    # Signals for updating state of state machine
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

        # Dictionary to hold labels once they are created
        self.label_dict = dict()
        # Lists hold gesture icon file names and gesture icon titles
        fileDir = os.path.dirname(os.path.abspath(__file__)) 
        self.image_list = [fileDir+'/images/index_up.png',fileDir+'/images/v_sign.png', fileDir+'/images/thumb_left.png',
                           fileDir+'/images/thumb_right.png', fileDir+'/images/fist.png', fileDir+'/images/five_wide.png',
                           fileDir+'/images/palm.png', fileDir+'/images/shaka.png']
        self.title_list = ['Move Up', 'Move Down', 'Move Left', 'Move Right', 'Zoom In',
                           'Zoom Out', 'Tilt Up', 'Tilt Down']
        # Create and add 6 labels containing hand gesture image to layout2 and 6
        # labels with the gesture descriptions to layout1
        for num in range(0, 8):
            # Each label is created to hold gesture icon image
            self.label = QLabel(self)
            # Pixmap is created with the current gesture icon image
            self.pixmap = QPixmap(self.image_list[num])
            # Breakpoints to scale size of gesture icons for different resolutions
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
            # Assigns gesture icon image to the current label
            self.label.setPixmap(self.pixmap)
            # Create gesture title label for the image
            self.label_title = QLabel(self.title_list[num])
            # Store current icon image label in dictionary
            self.label_dict[num] = self.label
            # Place current icon image label in layout
            self.layout2.addWidget(self.label_dict[num], alignment=QtCore.Qt.AlignCenter)
            # Place current icon image title label in layout
            self.layout1.addWidget(self.label_title, alignment=QtCore.Qt.AlignCenter)

        # Create state machine to reliably handle state changes during threading
        self.state_machine = QStateMachine()
        # Create button to handle state changes when pressed
        self.state_button = QPushButton(self)
        self.state_button.setStyleSheet("background-color: silver")
        # Connect button released signal to check_state slot
        self.state_button.released.connect(self.check_state)
        # Create on state for state machine
        self.on = QState()
        # Create off state for state machine
        self.off = QState()
        # Add transition for on state to off state when offSignal is emitted
        self.on.addTransition(self.offSignal, self.off)
        # Add transition for on state to on state when state_button clicked signal emitted
        self.on.addTransition(self.state_button.clicked, self.on)
        # Add transition for off state to on state when onSignal is emitted
        self.off.addTransition(self.onSignal, self.on)
        # Assign text property to state_button in on state
        self.on.assignProperty(self.state_button, "text", "Start Gesture Navigation")
        # Assign text property to state_button in off state
        self.off.assignProperty(self.state_button, "text", "Stop Gesture Navigation")
        # Add off state to state machine
        self.state_machine.addState(self.off)
        # Add on state to state machine
        self.state_machine.addState(self.on)
        # Set state machine initial state to on
        self.state_machine.setInitialState(self.on)
        # State state machine
        self.state_machine.start()
        # Create gesture tips button and connect it to start_gesture_tips slot
        self.tips_button = QPushButton("Gesture Navigation Tips")
        self.tips_button.setStyleSheet("background-color: silver")
        self.tips_button.pressed.connect(self.start_gesture_tips)
        # Create exit button and connect it to exit slot
        self.exit_button = QPushButton("Exit Program")
        self.exit_button.setStyleSheet("background-color: silver")
        self.exit_button.pressed.connect(self.exit)
        # Add tips, state, and exit button to layout 3
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
        """
        Function to create a pop up window that blocks the event loop until it is closed.
        Used to send info or warning messages.

        Parameters:
            title (string) : Title of pop up window
            message (string) : Body text of pop up window
            icon : QMessageBox icon to be displayed
        """
        # Create QMessageBox for pop up message
        self.popup_window = QMessageBox()
        # Set pop up title to passed in title
        self.popup_window.setWindowTitle(title)
        # Set pop up body text to passed in message
        self.popup_window.setText(message)
        # Set pop up icon to passed in icon
        self.popup_window.setIcon(icon)
        # Set pop up window to use Ok close button
        self.popup_window.setStandardButtons(QMessageBox.Ok)
        # Execute pop up window so that it blocks GUI loop until closed
        self.popup_window.exec()

    # Check state of state machine, take actions based on current state
    def check_state(self):
        """
        Function to check the current state of the state machine. Calls check_earth_tips
        if in on state, calls stop_opencv if in off state.
        """
        current_state = self.state_machine.configuration()

        if self.on in current_state:
            self.check_earth_tips()
        elif self.off in current_state:
            self.stop_opencv()

    def start_gesture_tips(self):
        """
        Function to create PyHand Earth gesture navigation tips window.
        """
        # Sets title of pop up window
        self.popup_title = "Welcome to PyHand Earth!"
        # Sets body text of pop up window
        self.popup_text = """\nThis program allows you to navigate the Google Earth Pro desktop application using only your Webcam and eight hand gestures.
                             \n\t       Instructions and Tips 
                             \n\nFor the best experience, please read the instructions below and then close this window: 
                             \n\n1. Position your webcam so that you have a blank, light-colored background behind you. 
                             \n\n2. Position your right hand and desired gesture in front of the webcam so that it fills a good portion of the orange bounding rectangle in the live video window once it opens. 
                             \n\n3. If the prediction is stuck on the wrong gesture, just shake your hand a little and let it reset. 
                             \n\n4. If you remove your hand completely and have a blank background, navigation should halt. 
                             \n\n5. Happy navigating! """
        # Calls show_popup to create pop up window
        self.show_popup(self.popup_title, self.popup_text, QMessageBox.Information)


    def check_earth_tips(self):
        """
        Called by check_state when state machine is in on state. Checks to see if Google Earth
        Start-up Tips window is open, and asks user to close the window with a pop up window
        message. If Google Earth Start-up Tips window is closed, calls open_camera.
        """
        # Checks if Google Earth start-up tips window is open
        if self.google_earth.start_up_tips():
            # Sets title of pop up window
            self.popup_title = "Gesture Navigation Warning Message"
            # Sets body text of pop up window
            self.popup_text = "Please make sure the Start-up Tips window is closed before " + \
                              "starting gesture navigation"
            # Calls show_popup to create pop up window
            self.show_popup(self.popup_title, self.popup_text, QMessageBox.Warning)
        else:
            # If Google Earth start-up tips window now open, calls open_camera
            self.open_camera()

    def open_camera(self):
        """
        Function to create OpenCV VideoCapture object. If camera is not found, creates pop up window
        message to warn user and ask them to connect a camera. If camera is found, calls
        start_opencv.
        """
        # Creates cv2 VideoCapture object, passing in -1 to find first active camera
        self.camera = cv2.VideoCapture(-1)
        # If camera is not found, create pop up window to warn the user
        if self.camera is None or not self.camera.isOpened():
            # Sets title of pop up window
            self.popup_title = "No Camera Found Warning Message"
            # Sets body text of pop up window
            self.popup_text = "No camera has been detected. \n\nPlease connect a camera before " + \
                              "starting gesture navigation.\n"
            # Calls show_popup to create pop up window
            self.show_popup(self.popup_title, self.popup_text, QMessageBox.Warning)
        else:
            # If camera is found, calls start_opencv
            self.start_opencv()

    def start_opencv(self):
        """
        Function to start the OpenCV gesture navigation window. Repositions the Google Earth window
        to take up half of the screen, then calls create_opencv to instantiate QtCapture window. The
        CommandThread class object is then instantiated to begin sending commands generated in the
        CaptureThread class to Google Earth. The QtCapture window is then displayed. Finally, the
        offSignal is emitted to change the state machine to the off state and the tips_button is
        disabled to prevent tips from being shown while gesture navigation is active.
        """
        # Repositions Google Earth to take up one half of the available screen size
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
        # Show opencv window
        self.capture.show()
        # Emits offSignal to ensure button in correct state
        self.offSignal.emit()
        # Disable tips button while gesture navigation is active
        self.tips_button.setEnabled(False)

    def create_opencv(self):
        """
        Creates QtCapture window to display the OpenCV window frames. Resizes and repositions
        the QtCapture window based on current monitor resolution.
        """
        # Create QtCapture window for rendering opencv window
        self.capture = QtCapture(self.desktop, self.screen, self.camera)
        self.capture.setParent(self.widget)
        self.capture.setWindowFlags(QtCore.Qt.Tool)
        self.capture.setWindowTitle("OpenCV Recording Window")
        # Get new height based on available screen space minus an offset for the window title
        new_height = int((self.desktop.height() * 3/4) - 35)
        # Get width that is half of the available screen space
        half_width = int(self.desktop.width() / 2)
        # Breakpoints to resize and reposition QtCapture window based on current monitor resolution
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
        Function to close the QtCapture OpenCV window and stop commands being sent to Google
        Earth.
        """
        # Sends request to end the Google Earth command thread
        self.command_thread.end_thread()
        time.sleep(1)

        # If capture object exists, end thread, release camera, and close window
        if self.capture:
            self.capture.stop_thread()
            time.sleep(1)
            self.capture.delete()
            self.capture.setParent(None)
        # Repositions Google Earth to take up full width of available screen space
        self.google_earth.reposition_earth_large()
        # Emits onSignal to ensure button in correct state
        self.onSignal.emit()
        # Enable tips when gesture navigation is not active
        self.tips_button.setEnabled(True)

    def exit(self):
        """
        Slot function for exit button signal. Stops commands being sent to Google Earth,
        ends the OpenCV window thread if running, closes Google Earth, and exits the Qt
        application.
        """
        # If the command thread is running, request thread end
        if self.command_thread:
            self.command_thread.end_thread()
            time.sleep(1)

        # If the capture thread is running, request thread end
        if self.capture:
            self.capture.stop_thread()
            time.sleep(1)
        # Close the Google Earth window
        self.google_earth.close_earth()
        # Quit the Qt application, returning to main
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

    # Get available desktop geometry
    desktop_widget = app.desktop()
    desktop_geometry = desktop_widget.availableGeometry()
    # Get total screen geometry
    screen_geometry = desktop_widget.screenGeometry()

    # Start Google Earth
    google_earth = GoogleEarth(desktop_geometry, screen_geometry)
    google_earth.initialize_google_earth()

    # Create Main Window and show it
    window = MainWindow(google_earth, desktop_geometry, screen_geometry)
    window.show()
    # Reposition gesture icon window based on current resolution
    x_position = screen_geometry.width() - desktop_geometry.width()
    y_position = desktop_geometry.bottom() - window.height()

    # Gesture icon window moved to bottom of screen
    window.move(x_position, y_position)
    # Executes Qt application
    app.exec_()
    # Exit program after GUI finished, needed for program to close
    # successfully after packaging. This will throw an exception in
    # VS Code, which is a VS Code bug and can be safely ignored.
    sys.exit()

if __name__ == '__main__':
    main()
