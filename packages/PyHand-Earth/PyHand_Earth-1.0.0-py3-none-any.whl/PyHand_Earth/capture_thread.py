import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage

class CaptureThread(QThread):
    updatePixmap = pyqtSignal(QPixmap)
    updateOutput = pyqtSignal(str)

    def __init__(self, earth, model, class_names, camera, desktop, screen):
        super(CaptureThread, self).__init__()

        self.desktop_geometry = desktop
        self.screen_geometry = screen
        self.camera = camera
        self.output = ""
        self.thread_running = True

        self.model = model
        self.class_names = class_names

        self.earth_commands = earth

        self.new_height = (self.desktop_geometry.height() * 3/4) - 35

        if self.screen_geometry.width() > 1280:
            self.new_width = int(self.desktop_geometry.width() / 2)
        elif self.screen_geometry.width() > 1152:
            self.new_width = int((self.desktop_geometry.width() * 28/64))
        elif self.screen_geometry.width() > 1024:
            self.new_width = int((self.desktop_geometry.width() * 23/64))
        else:
            self.new_width = int((self.desktop_geometry.width() * 17/64))

        self.frame_width = int(self.new_width)
        self.frame_height = int(self.new_height)

        self.rectangle_start = (int(self.frame_width * 1/2), int(self.frame_height * 1/8))
        self.rectangle_end = (int(self.frame_width * 31/32), int(self.frame_height * 7/8))

        self.text_start = (int(self.frame_width * 1/32), int(self.frame_height * 1/4))

        self.width = 96
        self.height = 96
        self.output = ''

    def run(self):

        while (not self.isInterruptionRequested()):
            _, frame = self.camera.read()

            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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

                # Add text
                type_1_text = '{}: {}%'.format("Move Up", int(type_1_pred*100))

                cv2.putText(frame, type_1_text, self.text_start,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add text
                type_2_text = '{}: {}%'.format("Move Down", int(type_2_pred*100))

                cv2.putText(frame, type_2_text, (self.text_start[0], self.text_start[1] + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add text
                type_3_text = '{}: {}%'.format("Move Left", int(type_3_pred*100))

                cv2.putText(frame, type_3_text, (self.text_start[0], self.text_start[1] + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add text
                type_4_text = '{}: {}%'.format("Move Right", int(type_4_pred*100))

                cv2.putText(frame, type_4_text, (self.text_start[0], self.text_start[1] + 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add text
                type_5_text = '{}: {}%'.format("Zoom In", int(type_5_pred*100))

                cv2.putText(frame, type_5_text, (self.text_start[0], self.text_start[1] + 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add text
                type_6_text = '{}: {}%'.format("Zoom Out", int(type_6_pred*100))

                cv2.putText(frame, type_6_text, (self.text_start[0], self.text_start[1] + 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add text
                type_7_text = '{}: {}%'.format("Tilt Up", int(type_7_pred*100))

                cv2.putText(frame, type_7_text, (self.text_start[0], self.text_start[1] + 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add text
                type_8_text = '{}: {}%'.format("Tilt Down", int(type_8_pred*100))

                cv2.putText(frame, type_8_text, (self.text_start[0], self.text_start[1] + 210),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)

                # Add text
                type_9_text = '{}: {}%'.format("Stop Motion", int(type_9_pred*100))

                cv2.putText(frame, type_9_text, (self.text_start[0], self.text_start[1] + 240),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (240, 240, 240), 2)


                if (not self.isInterruptionRequested()):
                    # Convert frame to PyQt format
                    img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    pix = QPixmap.fromImage(img)

                    # Emit PyQt signal, sending frame as a QPixmap
                    self.updatePixmap.emit(pix)

                #=======================================================
                # Below code section is for output to pautogui keyboard shortcuts

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
        # self.thread_running = False
        self.requestInterruption()
        self.wait()
        del self

    def release_camera(self):
        self.camera.release()
