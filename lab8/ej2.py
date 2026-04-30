import cv2

class process:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.filtro = "normal"

    def habilitar_camara(self):
        if not self.capture.isOpened():
            print("No se pudo abrir la camara")
            exit()

        while True:
            ret, frame = self.capture.read()

            if not ret:
                print("No se pudo leer el frame")
                break

            tecla = cv2.waitKey(1) & 0xFF

            if tecla == ord('a'):
                self.filtro = "gris"
                print("Filtro gris activado")

            elif tecla == ord('b'):
                self.filtro = "bordes"
                print("Filtro bordes activado")

            elif tecla == ord('c'):
                self.filtro = "threshold"
                print("Filtro threshold activado")

            elif tecla == ord('n'):
                self.filtro = "normal"
                print("Vista normal activada")

            elif tecla == ord('q'):
                break

            frame_filtrado = self.aplicar_filtro(frame)

            cv2.imshow("Webcam", frame_filtrado)

        self.capture.release()
        cv2.destroyAllWindows()

    def aplicar_filtro(self, frame):
        if self.filtro == "gris":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        elif self.filtro == "bordes":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            bordes = cv2.Canny(gray, 100, 200)
            return cv2.cvtColor(bordes, cv2.COLOR_GRAY2BGR)

        elif self.filtro == "threshold":
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        else:
            return frame


def menu():
    camara = process()

    print("Menu:")
    print("Habilitar camara: 1")
    print("Salir: 2")

    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        print("Controles en la ventana de la camara:")
        print("a: escala de grises")
        print("b: bordes")
        print("c: threshold")
        print("n: normal")
        print("q: salir")
        camara.habilitar_camara()

    elif opcion == "2":
        print("Saliendo...")
        exit()


if __name__ == "__main__":
    while True:
        menu()