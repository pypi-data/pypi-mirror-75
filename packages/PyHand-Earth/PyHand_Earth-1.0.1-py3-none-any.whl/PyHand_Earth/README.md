
<a  href="https://i.ibb.co/vZDRYBW/main-shot.png"  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>
  

# PyHand-Earth 

  

>Welcome to <i>PyHand-Earth</i>!


  

## Contents 

 -  [Project Description and Overview](#project-description-and-overview)
 -  [Special Comments](#special-comments)
 -  [Setup and Installation](#setup-and-installation)
 -  [Executable Command to Run PyHand-Earth](#executable-command-to-run-pyhand-earth)
 -  [User Guide](#user-guide)
 -  [Screenshots](#screenshots)
 -  [GitHub Repository](#github-repository)
 -  [Team](#team)
 -  [License](#license)

---
  

## Project Description and Overview

PyHand-Earth is a Python-based software project that incorporates and integrates multiple high-performant concepts, libraries, tools, and techniques to optimize and maximize user experience in navigating the Google Earth Pro Desktop application relying only on simple hand gestures and an ordinary Webcam.

As a programming language, Python owes much of its popularity to its predilection for rapid deployment and to the ever-growing ecosystem of third-party open-source libraries and tools that add scalability, thereby freeing up precious time to more directly focus energies on solving the problems around us.  Yet, that type of flexibility comes with a price - which is paid in the currency of performance.  However, there is no shortage of high-performant tools and libraries that leverage all that Python has to offer with the inherent speed of these optimized solutions, many of which are written in high-performing languages such as C++.

Despite advances in computer vision and deep learning neural networks, there are not many open-source software deployments that advance hand-gesture recognition in any appreciable direction towards the kinds of user interfaces depicted in movies such as those in the Marvel universe ... think Tony Stark navigating a holographic interface.  Those that do exist seem to require the use of special hardware that includes depth sensors (e.g., Microsoft's Xbox Kinect and ultraleap's Leap Motion controllers).

This project serves as an attempt to take a first step towards user interfaces of the future but without having to rely on such specialized hardware.

---

## Special Comments

For a smooth experience, users should review the following special comments, which include important instructions, tips, and suggestions.

- This project is designed to run on a dedicated Linux (Ubuntu 20.04) machine.  Because of certain limitations that are inherent with Virtual Boxes and Microsoft's Windows Subsystem for Linux (WSL), Webcams cannot be counted on to reliably operate on these substitute platforms.
- During the setup, installation, and startup, multiple libraries upon which the program is dependent will have to be downloaded, and so please be a little patient during this process.
- As noted further below, due to dependencies that are required in order for the principal pip installed libraries to <i>play nice together</i>, certain other libraries will need to be apt-get installed (as previously cleared by J.B.).
- This package requires Google Earth Pro desktop to be installed on the local machine.  If it is not already installed, the Google Earth Pro application automatically will be installed the first time you run the program.  A relatively large neural network learning model .h5 file also will be downloaded.  Consequently, please make allowances the first time you run the program.
- This project requires many other pip3 installed high-performant libraries to work in unison, which due to all the threading involved, was not the easiest task to accomplish.  Therefore, please also be patient while these libraries load and initialize.  Whereas some projects may require only one or two such libraries, this one incorporates TensorFlow/Keras, OpenCV, PyQt, maplotlib, and numpy, among others.  Consequently, it may take a few seconds for the user interface to fully load, and for certain video windows to open and close.
- Before running the program, all open applications should be closed, except for a terminal window, of course.  For best performance, this terminal window should not be maximized and instead should be kept to a reasonable size so that it does not interfere with the user interface.
- Because of the inherent physical limitations of ordinary Webcams, the hand gesture prediction will work most accurately when a blank, light-colored (e.g., white or cream) wall is positioned behind the user.
- There are eight available hand gestures to control navigation in Google Earth.  For a smoother experience, a few moments should be taken to familiarize yourself with these different gestures.  These gestures, together with their corresponding navigation motions, will be displayed once the program runs.
- When starting gesture navigation, the user's hand should be positioned so that it fills a good portion of the orange bounding rectangle in the live video window once it opens.
- In the event the prediction gets stuck on the wrong gesture, merely shake your hand a little and let it reset until the desired motion is achieved.  The learning model is based on over 26,000 images, but the limitation of ordinary Webcams, when coupled with varied lighting, backgrounds, and skin tones, can sometimes result in incorrect predictions, which easily can be reset as described.
- If you remove your hand completely such that only a blank wall occupies the orange bounding rectangle, all navigation and motion should halt.
- In case you need a refresher on the above, the program includes a "Gesture Navigation Tips" button that will display the most important tips.
- For academic purposes (as discussed in advance with J.B.), the live video window also contains text displaying the deep learning model's prediction values for each of the available eight hand gestures, as well as that for a blank wall.  (A future, non-academic, deployment instead will just display the controlling navigation motion in order to simplify the user's experience.)
- The GitHub repository root folder (under `master` branch) includes two sub-folders:
  - `new_main`:  Contains the most up-to-date files.
  - `old_code_structure`:  Archived files.
- A PDF file detailing contributions made outside of GitHub to this project is included in the `master` branch of the root folder.

---

## Setup and Installation

### Preliminary Matters

This project's installation package, and its dependencies, is hosted on PyPI at:

https://pypi.org/project/PyHand-Earth/


#### General Requirements

- Linux machine with Webcam
- Compatible with Ubuntu 20.04 installation
- Python 3.8 or higher 

#### Third-party pip installed library packages are included in setup.py as part of PyHand-Earth package install:

The following third-party packages automatically will be pip installed as part of the PyHand-Earth package pip install (as described further below):

- TensorFlow 2.2.0
- OpenCV 4.2.0.34
- matplotlib 3.2.2
- Keras 2.4.2
- pyautogui 0.9.50
- PyQt5
- psutil 5.7.0


#### Apt-get packages that must be independently installed due to required dependencies:

Although the libraries listed above that provide high-performant optimization all can be pip installed, there are unavoidable dependencies that the user must `apt-get` install in order for these libraries to coexist.  (Prior approvals have been obtained from J.B.).

The `apt-get` install commands that the user must execute from the command line for a proper PyHand-Earth installation are as follows:

```shell
$ sudo apt-get install python3-tk
```
(needed to pip install pyautogui)

```shell
$ sudo apt-get install python3-dev
```
(header files needed to pip install psutil)

```shell
$ sudo apt-get install libxcb-xinerama0
```
(required in order to start PyQt, which is pip installed)

```shell
$ sudo apt-get install wmctrl
```
(necessary to be able to manage certain windows)

```shell
$ sudo apt-get install scrot
```
(needed in order to locate images in the Google Earth application to ensure it behaves properly)



### PyHand-Earth pip installation package name

As documented at the PyPI repository page for PyHand-Earth, after the required dependencies described immediately above are installed, the software package can be installed from the command line with the following pip installation command:

```shell
$ pip3 install PyHand-Earth==1.0.1
```
Except as mentioned further below, this will install all the Python code developed for the project and third-party optimization libraries, as discussed previously above.


---

## Executable Command to Run PyHand-Earth

Once everything is installed, from the command line, simply run the following command to execute the PyHand-Earth program:

```shell
$ PyHand-Earth
```

As previously stated above, if you do not have the Google Earth Pro desktop application already installed on your local machine, the first time you run `PyHand-Earth`, the program will install the .deb package for Google Earth Pro.  In addition, it automatically will download from a google drive link a Keras .h5 file where the training model for the hand gesture recognition neural network is stored.


---

## User Guide

### Initial view upon start-up (with Google Earth Start up tips window closed)
<img  src=https://i.ibb.co/B2tB9MD/initial-view.png  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>

After launching the PyHand-Earth program, the user's initial view consists of the top portion of the display being filled by Google Earth and a smaller area at the bottom of the display featuring a graphical legend of eight hand gestures, as well as three user buttons.

<b><i>Tip</i></b>:  In the event Google Earth Pro launches a "Startup tips window", the user should close this window before proceeding.  Notwithstanding, in the event you forget to do so, you will be prompted at the appropriate time with a warning message.

The eight hand gestures, together with a blank wall (i.e., no hand gesture), and their corresponding navigation motions on Google Earth, are as follows:

| Hand Gesture			| Navigation Motion |
| ----------------------------- |:-----------------:|
| Index finger up		| Move Up	    |
| Peace sign      		| Move Down    	    |
| Left thumb extended		| Move Left    	    |
| Right thumb extended  	| Move Right   	    |
| Closed fist			| Zoom In	    |
| Five fingers opened wide  	| Zoom Out   	    |
| Open palm with fingers tight	| Tilt Up	    |
| Shaka "hang loose" sign  	| Tilt Down 	    |
| Blank wall			| No Motion	    |


For a smooth experience, you should take a few moments to familiarize yourself with these hand gestures and their motions.

Below the hand gesture icons, the user is presented with three buttons.  Clicking on any of these three buttons with the mouse will have the following functionality:

- `Gesture Navigation Tips`:  A pop-up window appears that provides the user with a handy list of tips to enhance the user's experience.
- `Start Gesture Navigation`:  Activates the Webcam, reduces the size of the Google Earth window to the left portion of the display, and opens a new live Webcam window to the right of the Google Earth window.  Clicking this button also alters the buttons as follows:
   - The `Start Gesture Navigation` label for the button is replaced with `Stop Gesture Navigation`, indicating a change of state for the button and providing the user with the means of closing the live Webcam window (upon which the state of the button reverts to its original one, and the size of the Google Earth window expands to occupy the display from left to right).
   - The `Gesture Navigation Tips` button is grayed out to mitigate the possibility of a pop-up window interfering with the hand gesture capturing process.
- `Exit Program`: Terminates the program.


Upon starting gesture navigation, an orange bounding rectangle is visible in the live Webcam video window.  By placing your <b><i>right</i></b> hand in the window and forming one of the eight gestures, you will be able to navigate Google Earth Pro.  One of the interesting features of this functionality is that Google Earth Pro's API was deprecated years ago, and so all navigation control is performed by optimized, threaded Python code.

<b><i>Tip</i></b>:  As mentioned previously, due to the physical limitations of ordinary Webcams, the prediction model works best when you have behind you a blank, light-colored wall.

To the left of the orange bounding rectangle, the neural network's prediction values for each of the motions (gestures) is displayed in text to the user (for academic evaluation purposes).

<b><i>Tip</i></b>:  In the event the prediction gets stuck on the wrong motion (gesture), simply shake your hand for a moment to allow the prediction to reset until the desired motion is achieved.

<b><i>Tip</i></b>:  If you remove your hand entirely so that the only thing in the orange bounding rectangle is a blank wall, all navigation and motion should stop.


---

## Screenshots

#### Gesture Navigation Tips pop-up window with helpful instructions and tips
<img  src=https://i.ibb.co/6vHqM3C/splash-tips.png  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>


#### Gesture navigation with index finger pointing up - Move Up
<img  src=https://i.ibb.co/BLDTXZx/index-up.png  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>


#### Gesture navigation with peace sign - Move Down
<img  src=https://i.ibb.co/FJg7Yx9/move-down.png  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>


#### Gesture navigation with left thumb extended - Move Left
<img  src=https://i.ibb.co/fQ4KQnM/move-left.png  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>


#### Gesture navigation with right thumb extended - Move Right
<img  src=https://i.ibb.co/NtVd115/move-right.png  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>


#### Gesture navigation with closed fist - Zoom In
<img  src=https://i.ibb.co/h7qtL1w/zoom-in.png  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>


#### Gesture navigation with five fingers opened wide - Zoom Out
<img  src=https://i.ibb.co/8YHMbFB/zoom-out.png  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>


#### Gesture navigation with open palm with fingers tight - Tilt Up
<img  src=https://i.ibb.co/bmJK82K/tilt-up.png  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>


#### Gesture navigation with Shaka "hang loose" sign - Tilt Down
<img  src=https://i.ibb.co/K2R9Czr/tilt-down.png  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>


#### Gesture navigation with blank wall (i.e., no hand gesture) - No Motion
<img  src=https://i.ibb.co/mybpvkF/blank-wall.png  title="# PyHand-Earth"  alt="# PyHand-Earth"></a>

---

## Team


- The PyHandlers team was formed for "CIS4930 - Performant Python Programming" from the University of Florida.

### Project team members:
- Grant H. Wise
- Tyler Allen
- Vanessa Orantes Murillo
- John Liu
- Ying Xu
 
---


## GitHub Repository

This README.md file and all other files and source code is located at the following GitHub Repository:

https://github.com/liujohnj/PyHand_Earth

Access has been furnished to J.B., N.S., and J.C.

---

## License

  

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

  

-  **[MIT license](http://opensource.org/licenses/mit-license.php)**

- Copyright © 2020  
