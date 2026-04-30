import cv2
import numpy as np

def read_colors(colors):
    for color in colors:
        mask = cv2.inRange(color["img"], color["lower"], color["upper"])
        total_pixels = mask.size
        matching_pixels = cv2.countNonZero(mask)
        if total_pixels == matching_pixels:
            print(color["name"])
        else:
            print("no es rosado, amarillo, ni verde")
        

if __name__ == "__main__":
    img1 = cv2.imread("pink.png")
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    img2 = cv2.imread("yellow.png")
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    img3 = cv2.imread("green.png")
    img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2HSV)

    pink_lower = np.array([140, 50, 50])
    pink_upper = np.array([170, 255, 255])
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    green_lower = np.array([36, 50, 50])
    green_upper = np.array([86, 255, 255])

    colors = [
        {"name": "rosado", "img": img1, "lower": pink_lower, "upper": pink_upper},
        {"name": "amarillo", "img": img2, "lower": yellow_lower, "upper": yellow_upper},
        {"name": "verde", "img": img3, "lower": green_lower, "upper": green_upper} 
    ]

    read_colors(colors)

    cv2.destroyAllWindows()