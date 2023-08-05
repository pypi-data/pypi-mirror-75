"""
File handler that downloads the files needed for program functionality
"""
import os.path
from shutil import which
import requests

class FileDownload():
    """
    This is a class that downloads files if they do not already exist in
    the supplied directory

    Attributes:
        model_url (str) : Static Google Drive url that hosts the .h5 file
        model_name (str) : Name of the model file being saved
        earth_url (str) : Static url that hosts the Google Earth deb file
        earth_name (str) : Name of the deb file to be saved
        current_directory (str) : Holds the string value of the current directory
        session : Instantiate Session class from requests
                response : Holds response object returned from HTTP request
        token (str) : Holds response token from Google Drive that is given when downloading
            large files
    """
    def __init__(self):
        """
        Please see help(FileDownload) for more info
        """
        self.model_url = 'https://drive.google.com/uc?export=download&id=18oXums8kjOF6iPw9iMwdXVlqqxswEiRm'
        self.model_name = '/pyearth_cnn_model_200612_1744.h5'
        self.earth_url = 'https://dl.google.com/dl/earth/client/current/google-earth-stable_current_amd64.deb'
        self.earth_name = '/google-earth-stable_current_amd64.deb'
        self.current_directory = ''
        self.session = requests.Session()
        self.response = None
        self.token = None
        self.chunk_size = 32768

    def get_drive_file(self):
        """
        Checks if model already exists in current directory. If it does not exist, downloads the
        model to the current directory.
        """
        # Gets current working directory and appends the target file name to it
        self.current_directory = os.getcwd() + self.model_name
        # Checks if the model file already exists in the current directory, returns if so
        if os.path.isfile(self.current_directory):
            return
        # Sends get request to Google Drive and stores response object
        self.response = self.session.get(self.model_url, stream=True)
        # If the file is large, a download warning is issued by Google Drive. Gets token
        # from this warning and stores it.
        for key, value in self.response.cookies.items():
            if key.startswith('download_warning'):
                token = value
                break
        # If the token exists, uses token to confirm large download.
        if token:
            params = {'confirm' : token}
            self.response = self.session.get(self.model_url, params=params, stream=True)
        # Opens current directory and saves model to it
        with open(self.current_directory, "wb") as my_file:
            for chunk in self.response.iter_content(self.chunk_size):
                if chunk:
                    my_file.write(chunk)

    def get_google_earth(self):
        """
        Checks if Google Earth is already installed. If not, creates google-earth folder
        in current directory and downloads the Google Earth deb to the new folder.

        Warning: If google-earth folder is created and file is downloaded there already,
        this will not install Google Earth. Please manually install using
        sudo dpkg -i google-earth-stable*.deb inside the relevant folder.
        """
        # Uses shutil which to determine if Google Earth is already installed
        if which('google-earth-pro') is not None:
            return
        # Creates path for new google-earth folder in current working directory
        self.current_directory = os.getcwd() + '/google-earth'
        # If google-earth folder does not exist, create it
        if not os.path.exists(self.current_directory):
            os.mkdir(self.current_directory)

        self.current_directory += self.earth_name
        # If Google Earth deb file is already downloaded in google-earth folder, return
        if os.path.isfile(self.current_directory):
            return
        # Sends get request and stores response object
        self.response = requests.get(self.earth_url)
        # Saves Google Earth deb file to current working directory/google-earth
        with open(self.current_directory, "wb") as my_file:
            my_file.write(self.response.content)
        # Google Earth deb has been downloaded if here, call function to install it
        self.install_google_earth()

    def install_google_earth(self):
        """
        Changes directory to google-earth folder, installs Google Earth deb, and
        returns to previous directory.
        """
        # Get current directory to return to
        self.current_directory = os.getcwd()
        # Change to google-earth folder
        os.chdir('google-earth')
        # Use dpkg to install Google Earth
        os.system('sudo dpkg -i google-earth-stable*.deb')
        # Return to previous directory
        os.chdir(self.current_directory)
