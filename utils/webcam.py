import cv2
from utils.common import cvToBase64


class Webcam:
    def __init__(self):
        self.webcam = cv2.VideoCapture(0)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 720)

    def getImage(self):
        ret, img = self.webcam.read()

        return cvToBase64(img)

    def release(self):
        self.webcam.release()
