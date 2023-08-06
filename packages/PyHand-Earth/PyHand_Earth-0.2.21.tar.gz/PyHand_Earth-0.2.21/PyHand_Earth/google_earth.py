"""
Implements the Google Earth class for interacting with Google Earth program.
"""
import os
import time
import psutil
from .keyboard_commands import KeyboardCommands

class GoogleEarth():
    """
    This is a class that starts Google Earth and performs operations
    on the Google Earth window.

    Attributes:
        keyboard_commands : Instantiates keyboard command class object for sending
            commands to Google Earth
        screen_position (list) : Position values for moving and resizing windows based
            on screen resolution
        resolution (string) : Resolution of the current monitor
    """
    def __init__(self, desktop_geo, screen_geo):
        """
        Please see help(GoogleEarth) for more info
        """
        self.keyboard_commands = KeyboardCommands()

        self.new_width = None
        self.new_height = None

        self.desktop_geometry = desktop_geo
        self.screen_geometry = screen_geo

    def check_process_running(self, process_name):
        """
        Checks if there are any processes currently running that contain a given name.

        Parameters:
        process_name (string) : Name of the process to be checked

        Returns:
        bool: Returns True if process found, else returns False
        """
        # Check if there is any running process that contains the given name processName.
        # Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def initialize_google_earth(self):
        """
        Checks if Google Earth is running and starts Google Earth if it is not running.
        Following start up, closes two Google Earth toolbars.
        """
        #Checking if Google Earth is already running
        if self.check_process_running('google-earth'):
            self.start_google_earth()

        else:
            #Start Google Earth if it is not already running and resize window
            os.system("nohup google-earth-pro </dev/null >/dev/null 2>&1 &")
            time.sleep(2)
            self.start_google_earth()

        self.toggle_buttons_off()

    def start_google_earth(self):
        """
        Gets the current screen resolution and starts Google Earth. Repositions Google Earth
        in the center of the screen with a size determined by the current screen resolution.
        """
        self.check_if_fullscreen()
        self.set_screen_resolution()
        comm = "wmctrl -r 'Google Earth' -e 0,0,0," + str(int(self.new_width)) + "," + \
                str(int(self.new_height))
        os.system(comm)
        time.sleep(2)

    def set_screen_resolution(self):
        """
        Sets the Google Earth window resize and screen position based on monitor resolution.
        """

        self.new_width = self.desktop_geometry.width()
        self.new_height = ((self.desktop_geometry.height() * (3/4)) - 37)

    def reposition_earth_small(self):
        # REPLACE with hotkey for ALT + F10 to toggle full screen
        self.check_if_fullscreen()

        comm = "wmctrl -r 'Google Earth' -e 0,0,0," + str(int(self.new_width / 2)) + "," + \
                str(int(self.new_height))
        os.system(comm)
        time.sleep(2)

    def reposition_earth_large(self):
        # REPLACE with hotkey for ALT + F10 to toggle full screen
        self.check_if_fullscreen()

        comm = "wmctrl -r 'Google Earth' -e 0,0,0," + str(int(self.new_width)) + "," + \
                str(int(self.new_height))
        os.system(comm)
        time.sleep(2)

    def toggle_buttons_off(self):
        """
        Toggles sidebar in Google Earth that cause problems when sending commands
        to the Google Earth window.
        """
        fileDir = os.path.dirname(os.path.abspath(__file__))
        sidebar_coords = self.keyboard_commands.locate_image(fileDir+'/images/clicked_sidebar.png')

        if sidebar_coords:
            self.keyboard_commands.close_sidebar()

    def start_up_tips(self):
        """
        Returns True/False flag to pop-up message to close Start-up Tips Google Earth Pro window.
        """
        fileDir = os.path.dirname(os.path.abspath(__file__))
        start_up_tips_coords = self.keyboard_commands.locate_image(fileDir+'/images/close.png')

        if start_up_tips_coords:
            return True
        else:
            return False

    def check_if_fullscreen(self):
        fileDir = os.path.dirname(os.path.abspath(__file__))
        fullscreen = self.keyboard_commands.locate_image(fileDir+'/images/fullscreen.png')

        if fullscreen:
            self.keyboard_commands.click_with_location(fullscreen)
            time.sleep(2)

    def close_earth(self):
        """
        Closes the Google Earth window.
        """
        os.system("wmctrl -c Google Earth Pro")
