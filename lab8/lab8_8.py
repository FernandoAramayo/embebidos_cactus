import cv2
import RPi.GPIO as GPIO

BUZZER = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUZZER, GPIO.OUT)

camara = cv2.VideoCapture(0)
fondo = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = camara.read()

    if ret == False:
        print("No se pudo leer la camara")
        break

    frame = cv2.resize(frame, (400, 300))

    mascara = fondo.apply(frame)

    pixeles_movimiento = cv2.countNonZero(mascara)

    if pixeles_movimiento > 5000:
        GPIO.output(BUZZER, GPIO.HIGH)
        print("Movimiento detectado")
    else:
        GPIO.output(BUZZER, GPIO.LOW)

    cv2.imshow("Camara", frame)
    cv2.imshow("Movimiento", mascara)

    tecla = cv2.waitKey(25)

    if tecla != -1:
        break

camara.release()
GPIO.output(BUZZER, GPIO.LOW)
GPIO.cleanup()
cv2.destroyAllWindows()