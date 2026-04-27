import cv2

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
            blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
            gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray_frame, 100, 200)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            valid_contours = [c for c in contours if cv2.contourArea(c) > 20]
            cv2.drawContours(frame, valid_contours, -1, (0, 255, 0), 3)
            cv2.imshow("camera", frame)
            key = cv2.waitKey(1)
            if key == 27:
                self.stop_display()
        

if __name__ == "__main__":
    camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
    camera_ob = video_capture(camera)
    camera_ob.display_camera()
