"""
Implements CommandThread to create a thread for sending current gesture
interpreted by machine learning model to Google Earth.
"""
from PyQt5.QtCore import QThread, pyqtSlot

class CommandThread(QThread):
    """
    Creates a QThread to get current gesture and output the gesture to
    Google Earth.

    Attributes:
        capture : QtCapture class object
        commands : KeyboardCommand class object

    Args:
        capture : QtCapture class object
        commands : KeyboardCommand class object
    """

    def __init__(self, capture, commands):
        """
        Please see help(CommandThread) for more info.
        """
        super(CommandThread, self).__init__()
        self.capture = capture
        self.commands = commands

    @pyqtSlot()
    def run(self):
        """
        Implements run of QThread object. Gets current navigation gesture interpreted
        by machine learning model, ends the previous commands, sets the new command to
        be the current gesture and then sends that gesture to Google Earth.
        """
        # While no interrupt requested
        while not self.isInterruptionRequested():
            # Get current gesture
            current_input = self.capture.get_output()
            # End current command
            self.commands.end_command()
            # Set new command to current gesture
            self.commands.set_command(current_input)
            # Send current gesture to Google Earth
            self.commands.send_command()

    def end_thread(self):
        """
        Ends thread safely by requested interruption and then deleting the thread.
        """
        # Request interruption to safely end thread
        self.requestInterruption()
        # Wait until request is acknowledged
        self.wait()
        # Send final "space" command to prevent gestures continuing in Google Earth
        self.commands.send_single_command("space")
        # Delete thread after interruption complete
        del self
