"""
Implements KeyboardCommands class to hold current navigation gesture and send commands to
Google Earth.
"""
import os
import pyautogui

class KeyboardCommands():
    """
    This class sets the current gesture navigation command, sends the current gesture to
    Google Earth, and checks if certain windows are displayed in Google Earth.

    Attributes:
        pyautogui.FAILSAFE : Sets pyautogui failsafe to false to disable full screen errors
        current_command (string) : Current gesture navigation command
    """

    def __init__(self):
        """
        Please see help(KeyboardCommands) for more info.
        """
        # Disable pyautogui failsafe to prevent problems when using fullscreen windows
        pyautogui.FAILSAFE = False
        # Current gesture navigation command
        self.__current_command = ''

    def set_command(self, cmd):
        """
        Setter for current gesture naviation command.

        Args:
            cmd (string) : Current gesture navigation command
        """
        # Sets the current gesture navigation command
        self.__current_command = cmd

    def send_single_command(self, cmd):
        """
        Sends a single command to Google Earth.

        Args:
            cmd (string) : Command to be send to Google Earth
        """
        # Target the Google Earth window
        os.system("wmctrl -a Google Earth Pro")
        # Send command
        pyautogui.press(cmd)

    def send_command(self):
        """
        Sends current command to Google Earth.
        """
        # Target Google Earth window
        os.system("wmctrl -a Google Earth Pro")
        # If current command is tilt_up, send hotkey for tilt up to
        # Google Earth
        if self.__current_command == 'tilt_up':
            pyautogui.keyDown('shift')
            pyautogui.keyDown('up')
        # Else If current command is tilt_down, send hotkey for tilt
        # down to Google Earth
        elif self.__current_command == 'tilt_down':
            pyautogui.keyDown('shift')
            pyautogui.keyDown('down')
        # Else send single current command to Google Earth
        else:
            pyautogui.keyDown(self.__current_command)

    def end_command(self):
        """
        Ends current command being sent to Google Earth.
        """
        # Target Google Earth window
        os.system("wmctrl -a Google Earth Pro")
        # If current command is tilt_up, end hotkey for tilt up
        if self.__current_command == 'tilt_up':
            pyautogui.keyUp('up')
            pyautogui.keyUp('shift')
        # Else If current command is tilt_down, end hotkey for tilt down
        elif self.__current_command == 'tilt_down':
            pyautogui.keyUp('down')
            pyautogui.keyUp('shift')
        # Else end single current command
        else:
            pyautogui.keyUp(self.__current_command)

    def close_sidebar(self):
        """
        Closes the Google Earth sidebar that prevents commands being
        sent correctly to Google Earth.
        """
        # Target the Google Earth window
        os.system("wmctrl -a Google Earth Pro")
        # Send a hotkey to Google Earth to close the toolbar
        pyautogui.hotkey('ctrlleft', 'Alt', 'b')

    def locate_image(self, img):
        """
        Searches Google Earth window for the provided image.

        Args:
            img : Image to search for in Google Earth window

        Returns:
            location : Returns location of image if image is found
            bool : Returns False if image not found
        """
        try:
            # Search Google Earth window for provided image
            location = pyautogui.locateOnScreen(img, confidence=0.9)
            # Return location of image if found
            return location
        # Catch OSError if image is not found
        except OSError:
            print(img + " Not Found")
            # Return False if image is not found
            return False

    def click_with_location(self, location):
        """
        Perform mouse click at provided location.

        Args:
            location : Location where mouse should click
        """
        # Performs mouse click at the location provided
        pyautogui.click(location)
