import cv2
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)

cap = cv2.VideoCapture(0)

bg = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=50,
    detectShadows=False
)

while True:
    ret, frame = cap.read()

    if not ret:
        print("errooooor")
        break

    mask = bg.apply(frame)

    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objetos = 0

    for c in contours:
        area = cv2.contourArea(c)

        if area > 1000:
            objetos += 1
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

    cv2.putText(frame, f"Objetos: {objetos}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if objetos == 0:
        ser.write(b'0')
    elif objetos == 1:
        ser.write(b'1')
    else:
        ser.write(b'2')

    cv2.imshow("Frame", frame)
    cv2.imshow("Mascara", mask)

    tecla = cv2.waitKey(1)

    if tecla == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()