from PyQt5.QtCore import QThread, pyqtSlot

class CommandThread(QThread):

    def __init__(self, capture, commands):
        super(CommandThread, self).__init__()
        self.capture = capture
        self.commands = commands
        self.issue_commands = True

    @pyqtSlot()
    def run(self):

        # While stop command false, get commands from hand_recognition
        # and send commands to Google Earth window
        while (not self.isInterruptionRequested()):
            current_input = self.capture.get_output()

            self.commands.end_command()
            self.commands.set_command(current_input)
            self.commands.send_command()

    def end_thread(self):
        self.requestInterruption()
        self.wait()
        self.commands.send_single_command("space")
        del self
