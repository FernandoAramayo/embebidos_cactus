import cv2
import os

class Capturador:
    def __init__(self):
        self.carpeta = "Captures"
        self.cap = cv2.VideoCapture(0)
        self.contador = 1

        os.makedirs(self.carpeta, exist_ok=True)

    def iniciar(self):
        if not self.cap.isOpened():
            print("No se pudo abrir la camara")
            exit()

        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("No se pudo leer el frame")
                break

            cv2.imshow("Webcam", frame)

            tecla = cv2.waitKey(1) & 0xFF

            if tecla == ord('c'):
                self.guardar_imagen(frame)

            elif tecla == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

        self.procesar_imagenes()

    def guardar_imagen(self, frame):
        nombre = f"image{self.contador}"
        carpeta_imagen = os.path.join(self.carpeta, nombre)

        os.makedirs(carpeta_imagen, exist_ok=True)

        ruta = os.path.join(carpeta_imagen, f"{nombre}.jpg")

        cv2.imwrite(ruta, frame)
        print(f"Imagen guardada: {ruta}")

        self.contador += 1

    def procesar_imagenes(self):
        for i in range(1, self.contador):
            nombre_base = f"image{i}"
            carpeta_imagen = os.path.join(self.carpeta, nombre_base)
            ruta = os.path.join(carpeta_imagen, f"{nombre_base}.jpg")

            imagen = cv2.imread(ruta)

            if imagen is None:
                print(f"No se pudo leer {ruta}")
                continue

            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(carpeta_imagen, f"{nombre_base}_gray.jpg"), gris)

            alto, ancho = gris.shape
            mitad_alto = alto // 2
            mitad_ancho = ancho // 2

            q1 = gris[0:mitad_alto, 0:mitad_ancho]
            q2 = gris[0:mitad_alto, mitad_ancho:ancho]
            q3 = gris[mitad_alto:alto, 0:mitad_ancho]
            q4 = gris[mitad_alto:alto, mitad_ancho:ancho]

            cv2.imwrite(os.path.join(carpeta_imagen, f"{nombre_base}_q1.jpg"), q1)
            cv2.imwrite(os.path.join(carpeta_imagen, f"{nombre_base}_q2.jpg"), q2)
            cv2.imwrite(os.path.join(carpeta_imagen, f"{nombre_base}_q3.jpg"), q3)
            cv2.imwrite(os.path.join(carpeta_imagen, f"{nombre_base}_q4.jpg"), q4)

            print(f"{nombre_base} procesada en gris y cuadrantes")


if __name__ == "__main__":
    programa = Capturador()
    programa.iniciar()