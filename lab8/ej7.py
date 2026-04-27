import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Variables
last_color = None

# Funciones
def get_colors(color_list):
    #red1_lower = np.array([0, 100, 100])
    #red1_upper = np.array([8, 255, 255])
    red2_lower = np.array([170, 150, 40])
    red2_upper = np.array([179, 255, 255])
    green_lower = np.array([36, 50, 50])
    green_upper = np.array([89, 255, 255])
    orange_lower = np.array([0, 150, 150])
    orange_upper = np.array([15, 255, 255])

    all_colors = [
        #{"name": "red", "lower": red1_lower, "upper": red1_upper},
        {"name": "red", "lower": red2_lower, "upper": red2_upper},
        {"name": "green", "lower": green_lower, "upper": green_upper},
        {"name": "orange", "lower": orange_lower, "upper": orange_upper}
    ]

    desired_colors = [color for color in all_colors if color["name"] in color_list]
    return desired_colors

def color_mask(img, *color_list):
    colors = get_colors(color_list)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_modified = np.zeros_like(img)
    for color in colors:
        mask = cv2.inRange(img_hsv, color["lower"], color["upper"])
        img_color = cv2.bitwise_and(img, img, mask=mask)
        img_modified = cv2.bitwise_or(img_modified, img_color)
    return img_modified

def check_color(img, *color_list):
    max_pixels = 0
    max_color = None
    colors = get_colors(color_list)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for color in colors:
        mask = cv2.inRange(img_hsv, color["lower"], color["upper"])
        matching_pixels = cv2.countNonZero(mask)
        if matching_pixels > max_pixels:
            max_pixels = matching_pixels
            max_color = color["name"]
    return max_color

def set_speed(color):
    global last_color
    speed = 0
    if last_color != color:
        match color:
            case "green":
                speed = 100
            case "orange":
                speed = 25
            case "red":
                speed = 0
        last_color = color
        print(f"{color}, speed = {speed}")
        motor_pwm.ChangeDutyCycle(speed)

def hardware_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    PWM_PIN = 18 
    DIR_PIN_1 = 23 
    DIR_PIN_2 = 24 

    GPIO.setup(PWM_PIN, GPIO.OUT)
    GPIO.setup(DIR_PIN_1, GPIO.OUT)
    GPIO.setup(DIR_PIN_2, GPIO.OUT)

    motor_pwm = GPIO.PWM(PWM_PIN, 1000)
    GPIO.output(DIR_PIN_1, GPIO.HIGH)
    GPIO.output(DIR_PIN_2, GPIO.LOW)    
    motor_pwm.start(0) 

    return motor_pwm

# Clases
class video_capture():
    def __init__(self, camera, motor):
        self.camera = camera
        self.displayed = False
        self.counter = 0
        self.color_buffer = []
        self.motor = motor
    
    def display_camera(self):
        self.displayed = True
        self.camera_visualization()

    def stop_display(self):
        self.displayed = False

    def camera_visualization(self):
        while self.displayed:
            _, frame = self.camera.read()

            # Obtener imagen filtrada con colores verde, naranja y rojo
            masked_frame = color_mask(frame, "green", "orange", "red")
            kernel = np.ones((15, 5), np.uint8)
            solid_mask = cv2.morphologyEx(masked_frame, cv2.MORPH_CLOSE, kernel)
            # Identificar contornos
            gray_frame = cv2.cvtColor(solid_mask, cv2.COLOR_BGR2GRAY)
            _, binary_mask = cv2.threshold(gray_frame, 1, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Identificar contorno mas grande y su color
            if len(contours) > 0:
                largest_contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest_contour) > 20:
                    # Convertir a negro todo excepto el contorno mas grande (led)
                    mask = np.zeros(binary_mask.shape[:2], dtype=np.uint8)
                    cv2.drawContours(mask, [largest_contour], -1, 255, thickness=-1)
                    result = cv2.bitwise_and(solid_mask, solid_mask, mask=mask)
                    cv2.imshow("camera", result)
                    led_color = check_color(result, "green", "orange", "red")
                    # Debounce 
                    if led_color is not None:
                        self.color_buffer.append(led_color)
                        if len(self.color_buffer) > 5:
                            self.color_buffer.pop(0)
                        if len(self.color_buffer) == 5 and len(set(self.color_buffer)) == 1:
                            set_speed(self.color_buffer[0])
                else:
                    cv2.imshow("camera", np.zeros_like(frame))
                    self.color_buffer.clear()
            else:
                cv2.imshow("camera", np.zeros_like(frame))
                self.color_buffer.clear()

            key = cv2.waitKey(1)
            if key == 27:
                self.stop_display()
        

# Main
if __name__ == "__main__":
    camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_EXPOSURE, 10) 

    motor_pwm = hardware_setup()

    camera_ob = video_capture(camera, motor_pwm)
    camera_ob.display_camera()

    motor_pwm.stop()
    del camera_ob.motor
    del motor_pwm
    GPIO.cleanup()
    print("Finished")
