import cv2 as cv
import numpy as np
import serial
import time

# 1. Configuración de la comunicación UART
try:
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
    print("Comunicación UART establecida.")
except Exception as e:
    print(f"Error al conectar UART: {e}")
    ser = None

# 2. Inicialización de Cámara y Sustractor de Fondo
cap = cv.VideoCapture(0)
fgbg = cv.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Procesamiento de Imagen y Filtros
    fgmask = fgbg.apply(frame)
    fgmask = cv.medianBlur(fgmask, 7)
    _, fgmask = cv.threshold(fgmask, 200, 255, cv.THRESH_BINARY)

    # 4. Detección de Contornos
    contours, _ = cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    ancho_total = frame.shape[1]
    alto_total = frame.shape[0]

    # --- Filtrar y contar objetos válidos ---
    objetos_validos = []
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 1500:  # Ignorar ruido
            objetos_validos.append(cnt)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

    cantidad_objetos = len(objetos_validos)
    msg = 'S'

    if cantidad_objetos == 0:
        msg = 'T'
        cv.putText(frame, "No object: Turning", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    elif cantidad_objetos >= 2:
        msg = 'M'
        cv.putText(frame, "Multiple objects: LEDs Toggle", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    elif cantidad_objetos == 1:
        cnt = objetos_validos[0]
        x, y, w, h = cv.boundingRect(cnt)
        cx = x + (w // 2)

        if cx < (ancho_total // 3):
            msg = 'L' 
            color = (255, 0, 0)
        elif cx > (2 * (ancho_total // 3)):
            msg = 'R' 
            color = (0, 0, 255)
        else:
            msg = 'F' 
            color = (0, 255, 0)
            cv.putText(frame, "Object Detected", (ancho_total - 200, alto_total - 20), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv.putText(frame, f"Tracking: {msg}", (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Resaltar el objeto seguido en verde


    if ser and ser.is_open:
        ser.write(msg.encode('utf-8'))

    cv.imshow('Sistema de Seguimiento', frame)
    cv.imshow('Mascara de Movimiento', fgmask)

    if cv.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
if ser: ser.close()
cv.destroyAllWindows()
