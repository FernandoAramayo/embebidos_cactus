import cv2 as cv
import numpy as np
import serial
import time

# 1. Configuración de la comunicación UART
# El puerto /dev/ttyS0 es común en Raspberry Pi para los pines GPIO 14/15
# Asegúrate de habilitar el puerto serial en raspi-config
try:
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
    print("Comunicación UART establecida.")
except Exception as e:
    print(f"Error al conectar UART: {e}")
    ser = None

# 2. Inicialización de Cámara y Sustractor de Fondo
cap = cv.VideoCapture(0)
# Se utiliza MOG2 para detectar movimiento separándolo del fondo [cite: 60, 145]
fgbg = cv.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Procesamiento de Imagen y Filtros
    # Aplicar sustractor para aislar el movimiento [cite: 144]
    fgmask = fgbg.apply(frame)
    
    # Aplicar Median Blur para eliminar ruido blanco ("sal y pimienta") [cite: 19, 84, 146]
    fgmask = cv.medianBlur(fgmask, 7)
    
    # Umbralizado para limpiar sombras detectadas por MOG2
    _, fgmask = cv.threshold(fgmask, 200, 255, cv.THRESH_BINARY)

    # 4. Detección de Contornos
    contours, _ = cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    movimiento_detectado = False
    ancho_total = frame.shape[1]
    alto_total = frame.shape[0]

    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 1500:  # Ignorar objetos pequeños [cite: 84]
            movimiento_detectado = True
            x, y, w, h = cv.boundingRect(cnt)
            cx = x + (w // 2)  # Centro horizontal del objeto [cite: 80]
            
            # Dibujar visualización
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # 5. Lógica de Control por Zonas [cite: 78, 148]
            if cx < (ancho_total // 3):
                msg = 'L'  # Izquierda
                color = (255, 0, 0)
            elif cx > (2 * (ancho_total // 3)):
                msg = 'R'  # Derecha
                color = (0, 0, 255)
            else:
                msg = 'F'  # Adelante / Centro
                color = (0, 255, 0)
                # Requisito ejercicio 2: "Object Detected" en el centro [cite: 64, 152]
                cv.putText(frame, "Object Detected", (ancho_total - 200, alto_total - 20), 
                           cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Enviar comando a la TIVA
            if ser and ser.is_open:
                ser.write(msg.encode('utf-8'))
            
            cv.putText(frame, f"Comando: {msg}", (x, y - 10), 
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Detener el loop de contornos tras detectar el objeto principal
            break 

    # 6. Si no hay movimiento, detener el robot (Opcional)
    if not movimiento_detectado and ser and ser.is_open:
        ser.write(b'S') # Comando personalizado para 'Stop'

    cv.imshow('Sistema de Seguimiento', frame)
    cv.imshow('Mascara de Movimiento', fgmask)

    if cv.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
if ser: ser.close()
cv.destroyAllWindows()
