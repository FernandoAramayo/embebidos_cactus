import cv2
import os
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la camara")
    exit()

contador = 1

while True:
    ret, frame = cap.read()

    if not ret:
        print("No se pudo leer el frame")
        break

    cv2.imshow("Webcam", frame)

    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord('c'):
        nombre_base = f"image{contador}"
        carpeta_captura = f"Capturesxd/{nombre_base}"
        ruta_original = f"{carpeta_captura}/{nombre_base}.jpg"
        cv2.imwrite(ruta_original, frame)

        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ruta_gris = f"{carpeta_captura}/{nombre_base}_gray.jpg"
        cv2.imwrite(ruta_gris, gris)

        alto, ancho = gris.shape
        mitad_alto = alto // 2
        mitad_ancho = ancho // 2

        q1 = gris[0:mitad_alto, 0:mitad_ancho]
        q2 = gris[0:mitad_alto, mitad_ancho:ancho]
        q3 = gris[mitad_alto:alto, 0:mitad_ancho]
        q4 = gris[mitad_alto:alto, mitad_ancho:ancho]

        cv2.imwrite(f"{carpeta_captura}/{nombre_base}_q1.jpg", q1)
        cv2.imwrite(f"{carpeta_captura}/{nombre_base}_q2.jpg", q2)
        cv2.imwrite(f"{carpeta_captura}/{nombre_base}_q3.jpg", q3)
        cv2.imwrite(f"{carpeta_captura}/{nombre_base}_q4.jpg", q4)

        print(f"Captura {contador} guardada en {carpeta_captura}")

        contador += 1

    elif tecla == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
