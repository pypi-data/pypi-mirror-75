"""
Implements CaptureThread to create a thread for rendering OpenCV frames
in the QtCapture window.
"""
import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage

class CaptureThread(QThread):
    """
    Creates a QThread to render and OpenCV frames and outputs gestures recognized
    by a machine learning model.

    Attributes:
        desktop_geometry : Available screen geometry based on current resolution
        screen_geometry : Total screen geometry based on current resolution
        camera: OpenCV camera object
        output (string) : Current gesture navigation output
        model : Machine learning model object
        class_names (list) : Contains names of gestures
        frame_height (int) : Height for repositioning frame
        frame_width (int) : Width for repositioning frame
        rectangle_start (tuple) : Starting x and y positions for ROI rectangle
        rectangle_end (tuple) : Ending x and y positions for ROI rectangle
        text_start (tuple) : Starting x and y positions for gesture text
        width (int) : Width for resizing ROI
        height (int) : Height for resisizng ROI

    Args:
        model : Machine learning model object
        class_names (list) : Contains names of gestures
        camera : OpenCV camera object
        desktop : Available screen geometry
        screen : Total screen geometry
    """
    # Signal for current frame
    updatePixmap = pyqtSignal(QPixmap)
    # Signal for current gesture
    updateOutput = pyqtSignal(str)

    def __init__(self, model, class_names, camera, desktop, screen):
        """
        Please see help(CaptureThread) for more info.
        """
        super(CaptureThread, self).__init__()
        # Available screen geometry
        self.desktop_geometry = desktop
        # Total screen geometry
        self.screen_geometry = screen
        # Holds OpenCV camera object
        self.camera = camera
        # Will hold output for current gesture
        self.output = ""
        # Holds machine learning model object
        self.model = model
        # List of names corresponding to gestures
        self.class_names = class_names
        # Sets new height for Google Earth to be 3/4 of available height minus offset
        # for window title
        self.frame_height = int((self.desktop_geometry.height() * 3/4) - 35)
        # Breakpoints for frame width based on width of current monitor resolution
        if self.screen_geometry.width() > 1280:
            self.frame_width = int(self.desktop_geometry.width() / 2)
        elif self.screen_geometry.width() > 1152:
            self.frame_width = int((self.desktop_geometry.width() * 28/64))
        elif self.screen_geometry.width() > 1024:
            self.frame_width = int((self.desktop_geometry.width() * 23/64))
        else:
            self.frame_width = int((self.desktop_geometry.width() * 17/64))
        # Sets rectangle starting positions based on current resolution
        self.rectangle_start = (int(self.frame_width * 1/2), int(self.frame_height * 1/8))
        # Sets rectangle ending positions based on current resolution
        self.rectangle_end = (int(self.frame_width * 31/32), int(self.frame_height * 7/8))
        # Sets gesture text starting positions based on current resolution
        self.text_start = (int(self.frame_width * 1/32), int(self.frame_height * 1/4))
        # Width used to resize ROI
        self.width = 96
        # Height used to resize ROI
        self.height = 96

    def run(self):
        """
        Implements run of QThread object. Gets camera frame using OpenCV, applies machine
        learning model to frame to interpret current gesture, then emits a QPixmap containing
        the frame to be drawn on QtCapture window and emits the current gesture.
        """

        while not self.isInterruptionRequested():
            # Create frame from camera
            _, frame = self.camera.read()

            if frame is not None:
                # Convert frame color
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Flip frame
                frame = cv2.flip(frame, 1)

                # Rescaling camera output
                frame = cv2.resize(frame, (self.frame_width, self.frame_height))

                # Add rectangle
                cv2.rectangle(frame, self.rectangle_start, self.rectangle_end, (240, 100, 0), 2)

                # Get ROI
                roi = frame[self.rectangle_start[1]:self.rectangle_end[1],
                            self.rectangle_start[0]:self.rectangle_end[0]]

                # Resize
                roi = cv2.resize(roi, (self.width, self.height))

                # Predict!
                roi_x = np.expand_dims(roi, axis=0)

                predictions = self.model.predict(roi_x)

                type_1_pred, type_2_pred, type_3_pred, \
                type_4_pred, type_5_pred, type_6_pred, \
                type_7_pred, type_8_pred, type_9_pred = predictions[0]

                # Add Move Up text to OpenCV window
                type_1_text = '{}: {}%'.format("Move Up", int(type_1_pred*100))

                cv2.putText(frame, type_1_text, self.text_start,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add Move Down text to OpenCV window
                type_2_text = '{}: {}%'.format("Move Down", int(type_2_pred*100))

                cv2.putText(frame, type_2_text, (self.text_start[0], self.text_start[1] + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add Move Left text to OpenCV window
                type_3_text = '{}: {}%'.format("Move Left", int(type_3_pred*100))

                cv2.putText(frame, type_3_text, (self.text_start[0], self.text_start[1] + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add Move Right text to OpenCV window
                type_4_text = '{}: {}%'.format("Move Right", int(type_4_pred*100))

                cv2.putText(frame, type_4_text, (self.text_start[0], self.text_start[1] + 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add Zoom In text to OpenCV window
                type_5_text = '{}: {}%'.format("Zoom In", int(type_5_pred*100))

                cv2.putText(frame, type_5_text, (self.text_start[0], self.text_start[1] + 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add Zoom Out text to OpenCV window
                type_6_text = '{}: {}%'.format("Zoom Out", int(type_6_pred*100))

                cv2.putText(frame, type_6_text, (self.text_start[0], self.text_start[1] + 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add Tilt Up text to OpenCV window
                type_7_text = '{}: {}%'.format("Tilt Up", int(type_7_pred*100))

                cv2.putText(frame, type_7_text, (self.text_start[0], self.text_start[1] + 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add Tilt Down text to OpenCV window
                type_8_text = '{}: {}%'.format("Tilt Down", int(type_8_pred*100))

                cv2.putText(frame, type_8_text, (self.text_start[0], self.text_start[1] + 210),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add Stop Motion text to OpenCV window
                type_9_text = '{}: {}%'.format("Stop Motion", int(type_9_pred*100))

                cv2.putText(frame, type_9_text, (self.text_start[0], self.text_start[1] + 240),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Prevent these commands if interrupt requested during loop
                if not self.isInterruptionRequested():
                    # Convert frame to PyQt format
                    img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    pix = QPixmap.fromImage(img)

                    # Emit PyQt signal, sending frame as a QPixmap
                    self.updatePixmap.emit(pix)

                # Emit string corresponding to current recognized gesture
                if type_1_pred > 0.90:
                    self.updateOutput.emit('up')
                elif type_2_pred > 0.90:
                    self.updateOutput.emit('down')
                elif type_3_pred > 0.90:
                    self.updateOutput.emit('left')
                elif type_4_pred > 0.90:
                    self.updateOutput.emit('right')
                elif type_5_pred > 0.90:
                    self.updateOutput.emit('=')
                elif type_6_pred > 0.90:
                    self.updateOutput.emit('-')
                elif type_7_pred > 0.90:
                    self.updateOutput.emit('tilt_up')
                elif type_8_pred > 0.90:
                    self.updateOutput.emit('tilt_down')
                elif type_9_pred > 0.90:
                    self.updateOutput.emit('spacebar')

    def stop_thread(self):
        """
        Ends thread safely by requested interruption and then deleting the thread.
        """
        # Request interruption to safely end thread
        self.requestInterruption()
        # Wait until request is acknowledged
        self.wait()
        # Delete thread after interruption complete
        del self

    def release_camera(self):
        """
        Releases camera object so it can be reused.
        """
        # Release camera object
        self.camera.release()
