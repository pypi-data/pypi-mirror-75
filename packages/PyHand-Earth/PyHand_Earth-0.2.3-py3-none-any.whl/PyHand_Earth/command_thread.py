from PyQt5.QtCore import QThread, pyqtSlot

class CommandThread(QThread):

    def __init__(self, capture, commands):
        super(CommandThread, self).__init__()
        self.capture = capture
        self.commands = commands
        self.issue_commands = True

    @pyqtSlot()
    def run(self):

        initial_input = self.capture.get_output()
        self.commands.set_command(initial_input)
        self.commands.send_command()
        # While stop command false, get commands from hand_recognition
        # and send commands to Google Earth window
        while self.issue_commands:
            current_input = self.capture.get_output()
            if current_input != initial_input:

                #self.commands.end_hotkey_command()
                self.commands.end_command()
                self.commands.set_command(current_input)
                self.commands.send_command()

                # if current_input == 'tilt_up':
                #     # self.commands.set_hotkey_command('shift', 'up')
                #     # self.commands.send_hotkey_command()
                #     self.commands.send_hotkey_two('shift', 'up')
                # elif current_input == 'tilt_down':
                #     # self.commands.set_hotkey_command('shift', 'down')
                #     # self.commands.send_hotkey_command()
                #     self.commands.send_hotkey_two('shift', 'down')
                # else:

        self.commands.send_single_command("space")

    def end_thread(self):
        self.issue_commands = False
