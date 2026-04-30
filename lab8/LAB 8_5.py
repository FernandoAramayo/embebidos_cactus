import cv2
import numpy as np

imagen = cv2.imread('watermelon.jpeg')

if imagen is None:
    print("Error")
else:
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    _, binarizada = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)

    contornos, jerarquia = cv2.findContours(binarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(imagen, contornos, -1, (0, 255, 0), 2)

    cv2.imshow('Ventana de Salida', imagen) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()