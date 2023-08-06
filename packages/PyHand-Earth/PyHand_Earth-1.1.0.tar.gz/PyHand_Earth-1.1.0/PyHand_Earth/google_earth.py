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
        keyboard_commands : KeyboardCommand class object
        new_width (int) : Width for repositioning Google Earth window
        new_height (int) : Height for repositioning Google Earth window
        desktop_geometry : Available screen geometry based on current resolution
        screen_geometry : Total screen geometry based on current resolution

    Args:
        desktop_geo : Available screen geometry
        screen_geo : Total screen geometry
    """
    def __init__(self, desktop_geo, screen_geo):
        """
        Please see help(GoogleEarth) for more info.
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
        Calls toggle_button_off to check if Google Earth toolbar is open.
        """
        #Checking if Google Earth is already running
        if self.check_process_running('google-earth'):
            self.start_google_earth()

        else:
            #Start Google Earth if it is not already running and resize window
            os.system("nohup google-earth-pro </dev/null >/dev/null 2>&1 &")
            time.sleep(2)
            self.start_google_earth()
        # Calls toggle_button_off to check if toolbar open
        self.toggle_button_off()

    def start_google_earth(self):
        """
        Checks if Google Earth is maximized and then sets width and height for positioning
        Google Earth. Repositions Google Earth to upper 3/4 of screen and resizes Google
        Earth to take up width of available screen.
        """
        # Calls check_if_fullscreen to check if Google Earth is maximized
        self.check_if_fullscreen()
        # Calls set_screen_resolution to set new width and height based on current resolution
        self.set_screen_resolution()
        # Sets command to reposition and resize Google Earth window
        comm = "wmctrl -r 'Google Earth' -e 0,0,0," + str(int(self.new_width)) + "," + \
                str(int(self.new_height))
        # Sends command to reposition and resize Google Earth window
        os.system(comm)
        # Pause to make sure command issued successfully
        time.sleep(2)

    def set_screen_resolution(self):
        """
        Sets the Google Earth window width and height values based on monitor resolution.
        """
        # Sets new width for Google Earth based on available screen width
        self.new_width = self.desktop_geometry.width()
        # Sets new height for Google Earth to be 3/4 of available height minus offset
        # for window title
        self.new_height = ((self.desktop_geometry.height() * (3/4)) - 37)

    def reposition_earth_small(self):
        """
        Checks if Google Earth is maximized, then repositions and resizes Google Earth to
        have half the width of current available screen space and 3/4 of available screen
        height.
        """
        # Checks if Google Earth is maximized
        self.check_if_fullscreen()
        # Sets command to reposition and resize Google Earth window
        comm = "wmctrl -r 'Google Earth' -e 0,0,0," + str(int(self.new_width / 2)) + "," + \
                str(int(self.new_height))
        # Sends command to reposition and resize Google Earth window
        os.system(comm)
        # Pause to make sure command issued successfully
        time.sleep(2)

    def reposition_earth_large(self):
        """
        Checks if Google Earth is maximized, then repositions and resizes Google Earth to
        have the fulls width of current available screen space and 3/4 of available screen
        height.
        """
        # Checks if Google Earth is maximized
        self.check_if_fullscreen()
         # Sets command to reposition and resize Google Earth window
        comm = "wmctrl -r 'Google Earth' -e 0,0,0," + str(int(self.new_width)) + "," + \
                str(int(self.new_height))
        # Sends command to reposition and resize Google Earth window
        os.system(comm)
        # Pause to make sure command issued successfully
        time.sleep(2)

    def toggle_button_off(self):
        """
        Closes sidebar in Google Earth that cause problems when sending commands
        to the Google Earth window.
        """
        # Checks to see if the Google Earth sidebar is open
        fileDir = os.path.dirname(os.path.abspath(__file__))
        sidebar_coords = self.keyboard_commands.locate_image(fileDir+'/images/clicked_sidebar.png')
        # If the sidebar is open, call close_sidebar to close it
        if sidebar_coords:
            self.keyboard_commands.close_sidebar()

    def start_up_tips(self):
        """
        Checks if Start-up Tips widnow is open in Google Earth.

        Returns:
            bool: Returns True if Google Earth Start Up Tips window open, else returns False
        """
        # Checks to see if Google Earth start up tips window is open
        fileDir = os.path.dirname(os.path.abspath(__file__))
        start_up_tips_coords = self.keyboard_commands.locate_image(fileDir+'/images/close.png')
        # If the Google Earth start up tips window is open, return True, else False
        if start_up_tips_coords:
            return True
        else:
            return False

    def check_if_fullscreen(self):
        """
        Checks if Google Earth window is maximized, which prevents Google Earth from
        receiving resize commands. If Google Earth window is maximized, minimizes the
        window.
        """
        # Checks if Google Earth window is maximized
        fileDir = os.path.dirname(os.path.abspath(__file__))
        fullscreen = self.keyboard_commands.locate_image(fileDir+'/images/fullscreen.png')
        # If the window is maximized, minimizes it
        if fullscreen:
            self.keyboard_commands.click_with_location(fullscreen)
            time.sleep(2)

    def close_earth(self):
        """
        Closes the Google Earth window.
        """
        os.system("wmctrl -c Google Earth Pro")
