import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

BUZZER = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

def activar_buzzer():
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(BUZZER, GPIO.LOW)


cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask= fgbg.apply(gray)

    kernel = np.ones((5,5), np.uint8)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    movimiento = False
    for cnt in contours:
        if cv2.contourArea(cnt) > 500: 
            movimiento = True
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    if movimiento:
        activar_buzzer()


    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", fgmask)

    if cv2.waitKey(30) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()