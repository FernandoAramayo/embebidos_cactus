import cv2
import numpy as np

cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=100, detectShadows=False)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
center_left_bound = width // 3
center_right_bound = 2 * (width // 3)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fgmask = fgbg.apply(frame)
    fgmask = cv2.GaussianBlur(fgmask, (13, 13), 0)
    kernel = np.ones((5, 5), np.uint8)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.dilate(fgmask, kernel, iterations=2)

    frame_sin_fondo = cv2.bitwise_and(frame, frame, mask=fgmask)

    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    object_in_middle = False

    for contour in contours:
        if cv2.contourArea(contour) > 15000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame_sin_fondo, (x, y), (x+w, y+h), (0, 255, 0), 2)
            object_center_x = x + (w // 2)

            if center_left_bound < object_center_x < center_right_bound:
                object_in_middle = True

    cv2.line(frame_sin_fondo, (center_left_bound, 0), (center_left_bound, height), (255, 0, 0), 1)
    cv2.line(frame_sin_fondo, (center_right_bound, 0), (center_right_bound, height), (255, 0, 0), 1)

    if object_in_middle:
        text = "Objeto detectado"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = width - text_size[0] - 20
        text_y = height - 20
        cv2.putText(frame_sin_fondo, text, (text_x, text_y), font, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)

    cv2.imshow('Deteccion de Objeto', frame_sin_fondo)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
