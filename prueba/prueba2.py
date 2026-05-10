import cv2 as cv
import numpy as np


class CaptureCamera:
    def __init__(self, cam):
        self.cam = cam

    def start_video(self):
        self.displayed = True
        self.show_video()

    def stop_video(self):
        self.displayed = False

    def show_video(self):
        #backSub = cv.createBackgroundSubtractorMOG2(detectShadows=False)
        while self.displayed:
            _, frame = self.cam.read()

            #fgmask = backSub.apply(frame)

            cv.imshow("frame", frame)


            key = cv.waitKey(1)
            if key == 27:
                self.stop_video()

def main():
    cam = cv.VideoCapture(0)
    cam_ob = CaptureCamera(cam)
    cam_ob.start_video()
    

if __name__ == "__main__":
    main()