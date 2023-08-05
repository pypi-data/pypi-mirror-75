"""
Implements the Google Earth class for interacting with Google Earth program.
"""
import os
import time
import psutil
from keyboard_commands import KeyboardCommands

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
    def __init__(self, desktop_geometry):
        """
        Please see help(GoogleEarth) for more info
        """
        self.keyboard_commands = KeyboardCommands()
        self.screen_position = []
        self.screen_resize = []
        self.desktop_geometry = desktop_geometry

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
        self.set_screen_resolution()
        comm = "wmctrl -r 'Google Earth' -e 0," + str(int(self.screen_position[0])) + "," + \
                str(int(self.screen_position[1])) + "," + str(int(self.screen_resize[0])) + "," + \
                str(int(self.screen_resize[1]))
        os.system(comm)
        time.sleep(2)

    def set_screen_resolution(self):
        """
        Sets the Google Earth window resize and screen position based on monitor resolution.
        """
        #print(self.desktop_geometry.width(), self.desktop_geometry.height())
        self.screen_resize.append(self.desktop_geometry.width() * (2/5))
        self.screen_resize.append(self.desktop_geometry.height() * (2/5))

        #print(self.screen_resize[0], self.screen_resize[1])

        self.screen_position.append((self.desktop_geometry.width()/2)-(self.screen_resize[0]/2))
        self.screen_position.append((self.desktop_geometry.height()/2)-(self.screen_resize[1]/2))



    def toggle_buttons_off(self):
        """
        Toggles two toolbars in Google Earth that cause problems when sending commands
        to the Google Earth window.
        """
        sidebar_coords = self.keyboard_commands.locate_image('images/close.png')

        if sidebar_coords:
            self.keyboard_commands.click_with_location(sidebar_coords)
            time.sleep(2)

        sidebar_coords = self.keyboard_commands.locate_image('images/clicked_sidebar.png')

        if sidebar_coords:
            self.keyboard_commands.click_with_location(sidebar_coords)
            time.sleep(2)

    def get_screen_resize(self):
        """
        Returns the values used to resize the Google Earth window.

        Returns:
            resolution (str) : Current Google Earth window size.
        """
        return self.screen_resize

    def get_screen_position(self):
        """
        Returns the Google Earth window X and Y positions.

        Returns:
            screen_position (list) : X and Y positions determined by current screen resolution.
        """
        return self.screen_position

    def close_earth(self):
        """
        Closes the Google Earth window.
        """
        os.system("wmctrl -c Google Earth Pro")
