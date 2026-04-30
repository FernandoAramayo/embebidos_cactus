import cv2
from abc import ABC, abstractmethod

class VideoBase(ABC):

    @abstractmethod
    def show(self):
        pass

class VideoCamera(VideoBase):

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mode = "gray"

    def show(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            if self.mode == "gray":
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif self.mode == "rgb":
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            cv2.imshow("Camera", img)

            key = cv2.waitKey(1)

            if key == ord('g'):
                self.mode = "gray"
                print("GRAY")

            elif key == ord('r'):
                self.mode = "rgb"
                print("RGB")

            elif key == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    cam = VideoCamera()
    cam.show()