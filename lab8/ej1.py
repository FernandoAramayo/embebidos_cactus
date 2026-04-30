import cv2
import numpy as np

cap = cv2.VideoCapture('video.mp4')

if not cap.isOpened():
    print("Error")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Resize: Video completo a 400x600
    resized = cv2.resize(frame, (400, 600))

    # 2. Edge Detector
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    # 3. Divide the video in two halves (Vertical Split)
    half_width = 400 // 2
    left_half = resized[:, :half_width]
    right_half = resized[:, half_width:]

    # 4. Divide into Quadrants
    quad_small = cv2.resize(resized, (200, 300))
    top_row = np.hstack((quad_small, quad_small))
    bottom_row = np.hstack((quad_small, quad_small))
    quadrants = np.vstack((top_row, bottom_row))

    cv2.imshow('1. Resized Video', resized)
    cv2.imshow('3a. Left Half', left_half)
    cv2.imshow('3b. Right Half', right_half)
    cv2.imshow('2. Edge Detector', edges)
    cv2.imshow('4. Quadrants', quadrants)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()