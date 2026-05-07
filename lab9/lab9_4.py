import cv2
import numpy as np

imagen = cv2.imread('fotos/monedas_2.jpg')
if imagen is None:
    print("Error")
    exit()

gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

gris_blur = cv2.medianBlur(gris, 15)

circulos = cv2.HoughCircles(
    gris_blur, 
    cv2.HOUGH_GRADIENT, 
    dp=1,            
    minDist=300,      
    param1=50,     
    param2=25,      
    minRadius=120,    
    maxRadius=250    
)

monedas_detectadas = 0

if circulos is not None:

    circulos = np.uint16(np.around(circulos))
    
    for c in circulos[0, :]:
        x, y, r = c[0], c[1], c[2] 
        
        cv2.circle(imagen, (x, y), r, (0, 255, 0), 3)
        
        cv2.circle(imagen, (x, y), 2, (0, 0, 255), 3)
        
        monedas_detectadas += 1

cv2.putText(imagen, f'Monedas detectadas: {monedas_detectadas}', (20, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

cv2.imshow("Resultado HoughCircles", imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()