"""
Starts a Qt application that drives input and output from an opencv window to the Google Earth
program
"""
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, \
     QPushButton, QWidget, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThreadPool, QStateMachine, QState

from keyboard_commands import KeyboardCommands
from google_earth import GoogleEarth
from capture_window import QtCapture
from file_download import FileDownload
from command_thread import CommandThread

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
    def __init__(self, earth, *args, **kwargs):
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
        # Will hold thread for issuing GE commands
        self.command_thread = None
        # Make Qt gesture icon window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Get resolution, window size, and offsets for positioning
        self.google_earth = earth
        self.new_position = self.google_earth.get_screen_position()
        self.window_resize = self.google_earth.get_screen_resize()
        self.title_bar_offset = 35
        # Set geometry of Qt gesture icon window
        # (this window is the parent of all other Qt windows)
        self.setGeometry(QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
            # Width of Qt gesture window based on width of GE window
            QtCore.QSize(int(self.window_resize[0]), 100),
            QtWidgets.qApp.desktop().availableGeometry()))
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
        self.image_list = ['images/index_up.png', 'images/fist.png', 'images/palm.png', 'images/thumb_left.png',
                           'images/thumb_right.png', 'images/five_wide.png']
        self.title_list = ['Move Up', 'Zoom In', 'Placeholder', 'Move Left', 'Move Right',
                           'Zoom Out']
        # Create and add 6 labels containing hand gesture image to layout2 and 6
        # labels with the gesture descriptions to layout1
        for num in range(0, 6):

            self.label = QLabel(self)
            self.pixmap = QPixmap(self.image_list[num])
            self.pixmap = self.pixmap.scaledToWidth(100)
            self.label.setPixmap(self.pixmap)

            self.label_title = QLabel(self.title_list[num])
            # Modify left margins for images and labels positioning
            if num == 0:
                self.label.setContentsMargins(25, 0, 0, 0)
                self.label_title.setContentsMargins(35, 0, 0, 0)
            elif num == 5:
                self.label.setContentsMargins(25, 0, 0, 0)
                self.label_title.setContentsMargins(35, 0, 0, 0)
            else:
                self.label.setContentsMargins(15, 0, 0, 0)
                self.label_title.setContentsMargins(25, 0, 0, 0)

            self.label_dict[num] = self.label

            self.layout2.addWidget(self.label_dict[num])

            self.layout1.addWidget(self.label_title)

        # Create start button and connect it to start_opencv function
        self.start_button = QPushButton("Start Gesture Navigation")
        self.start_button.setStyleSheet("background-color: silver")
        self.start_button.pressed.connect(self.start_opencv)
        # Create stop button and connect it to stop_opencv function
        self.stop_button = QPushButton("Stop Gesture Navigation")
        self.stop_button.setStyleSheet("background-color: silver")
        self.stop_button.pressed.connect(self.stop_opencv)
        # Create stop button and connect it to stop_opencv function
        self.exit_button = QPushButton("Exit Program")
        self.exit_button.setStyleSheet("background-color: silver")
        self.exit_button.pressed.connect(self.exit)
        # Add start and stop button to layout 3
        self.layout3.addWidget(self.start_button)
        self.layout3.addWidget(self.stop_button)
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

    def start_opencv(self):
        """
        Slot function for the start button signal. Instantiates Qt opencv window if not created,
        then starts and shows the window. Once the window is opened, starts worker thread to send
        commands to Google Earth.
        """
        # If opencv window not created, create it
        if not self.capture:
            self.create_opencv()
        else:
            self.capture = None
            self.create_opencv()
        # Start video capture and show it
        self.capture.show()
        # If command thread exists, remove it
        if self.command_thread:
            self.command_thread = None
        # Start command thread for sending commands to GE
        self.command_thread = CommandThread(self.capture, self.commands)
        self.command_thread.start()

    def create_opencv(self):
        # Create QtCapture window for rendering opencv window
        self.capture = QtCapture(self.google_earth)
        self.capture.setParent(self.widget)
        self.capture.setWindowFlags(QtCore.Qt.Tool)
        self.capture.setWindowTitle("OpenCV Recording Window")
        self.capture.setGeometry(int(self.window_resize[0] + self.new_position[0]),
                                 int(self.window_resize[1] + self.title_bar_offset),
                                 -1, -1)

    def stop_opencv(self):
        """
        Slot function for stop button signal. Stops Qt timer in opencv loop and sets
        stop_commands to True to kill worker thread.
        """
        # Set flag to kill GE command thread
        self.command_thread.end_thread()
        # If capture object exists, end thread, release camera, and close window
        if self.capture:
            self.capture.stop_thread()
            self.capture.delete()
            self.capture.setParent(None)
        # Send last command as space to prevent continuous command in GE
        self.commands.set_command("space")
        self.commands.send_command()
        self.commands.end_command()

    def exit(self):
        """
        Slot function for exit button signal. Sets stop_commands to True to kill worker
        thread, then calls close_earth to close Google Earth window, and finally terminates
        the QApplication.
        """
        # Make sure a single command is sent and ended before exit
        self.commands.set_command("space")
        self.commands.send_command()
        self.commands.end_command()
        # Stop threads, close GE, and exit application
        if self.capture:
            self.capture.stop_thread()
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
    desktop_geometry = desktop_widget.screenGeometry()

    # Start Google Earth
    google_earth = GoogleEarth(desktop_geometry)
    google_earth.initialize_google_earth()

    # Create Main Window and show it
    window = MainWindow(google_earth)
    window.show()

    # Reposition main window
    screen_pos = google_earth.get_screen_position()
    screen_res = google_earth.get_screen_resize()

    x_position = int(screen_pos[0])
    y_position = int(screen_res[1]) + int(screen_pos[1])
    title_offset = 38

    # Window moved to x position of GE window,
    # y position of GE window + height of GE window
    window.move(x_position, y_position + title_offset)

    app.exec_()

if __name__ == '__main__':
    main()
