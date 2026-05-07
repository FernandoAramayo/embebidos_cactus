import cv2 as cv
import numpy as np

cap = cv.VideoCapture('recursos lab 9/bouncing.mp4.mp4')
 
backSub = cv.createBackgroundSubtractorMOG2(detectShadows=True)

while cap.isOpened():
    ret, frame = cap.read()
 
    if not ret:
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        continue

    fgmask = backSub.apply(frame)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    _, sat_mask = cv.threshold(s, 80, 255, cv.THRESH_BINARY)

    filtered_frame = cv.bitwise_and(fgmask, sat_mask)

    kernel = np.ones((5, 5), np.uint8)
    opened_mask = cv.morphologyEx(filtered_frame, cv.MORPH_OPEN, kernel)
    kernel = np.ones((11, 11), np.uint8)
    closed_mask = cv.morphologyEx(opened_mask, cv.MORPH_CLOSE, kernel)

    contours, _ = cv.findContours(closed_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contours:
                if cv.contourArea(c) > 1000:
                    x,y,w,h = cv.boundingRect(c)
                    cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
 
    cv.imshow('frame', frame)
    if cv.waitKey(1) == 27:
        break
 
cap.release()
cv.destroyAllWindows()