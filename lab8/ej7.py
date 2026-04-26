import cv2
from colors import color_mask

class video_capture():
    def __init__(self, camera):
        self.camera = camera
        self.displayed = False
    
    def display_camera(self):
        self.displayed = True
        self.camera_visualization()

    def stop_display(self):
        self.displayed = False

    def camera_visualization(self):
        while self.displayed:
            _, frame = self.camera.read()
            #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #edges = cv2.Canny(gray_frame, 100, 200)
            #contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
            masked = color_mask(frame, "green", "orange", "red")
            cv2.imshow("camera", masked)
            key = cv2.waitKey(1)
            if key == 27:
                self.stop_display()
        

if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    camera_ob = video_capture(camera)
    camera_ob.display_camera()
