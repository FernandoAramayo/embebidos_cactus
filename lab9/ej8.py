import cv2 as cv
import numpy as np

# Funciones
def get_colors(color_list):
    red1_lower = np.array([0, 100, 100])
    red1_upper = np.array([5, 255, 255])
    red2_lower = np.array([170, 100, 100])
    red2_upper = np.array([179, 255, 255])
    
    green_lower = np.array([36, 50, 50])
    green_upper = np.array([89, 255, 255])
    
    cian_lower = np.array([85, 100, 100])
    cian_upper = np.array([95, 255, 255])
    
    yellow_lower = np.array([25, 100, 100])
    yellow_upper = np.array([35, 255, 255])
    
    purple_lower = np.array([130, 100, 100])
    purple_upper = np.array([160, 255, 255])

    all_colors = [
        {"name": "red", "lower": red1_lower, "upper": red1_upper},
        {"name": "red", "lower": red2_lower, "upper": red2_upper},
        {"name": "green", "lower": green_lower, "upper": green_upper},
        {"name": "cian", "lower": cian_lower, "upper": cian_upper},
        {"name": "yellow", "lower": yellow_lower, "upper": yellow_upper},
        {"name": "purple", "lower": purple_lower, "upper": purple_upper}   
    ]

    desired_colors = [color for color in all_colors if color["name"] in color_list]
    return desired_colors

def get_binary_mask(img, color_name):
    colors = get_colors([color_name])
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    final_mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    for color in colors:
        mask = cv.inRange(img_hsv, color["lower"], color["upper"])
        final_mask = cv.bitwise_or(final_mask, mask)
        
    return final_mask

def identify_shape(contour):
    # Perimetro
    peri = cv.arcLength(contour, True)
    
    # Aproximar poligono con precision de 4% 
    approx = cv.approxPolyDP(contour, 0.04 * peri, True)
    
    # Contar esquinas
    corners = len(approx)
    
    if corners == 3:
        return "triangle"
    elif corners == 4:
        x, y, w, h = cv.boundingRect(approx)
        aspect_ratio = float(w) / h
        if 0.95 <= aspect_ratio <= 1.05:
            return "square"
        else:
            return "rectangle"
    elif corners == 5:
        return "pentagon"
    elif corners == 6:
        return "hexagon"
    else:
        return "circle"

# --- Main ---
img = cv.imread('recursos lab 9/figuras.png')
colors = ["red", "yellow", "purple", "cian", "green"]

for color in colors:
    binary_mask = get_binary_mask(img, color)
    
    contours, _ = cv.findContours(binary_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    for c in contours:
        if cv.contourArea(c) > 500:     
            shape_name = identify_shape(c)
            print(f"{color} {shape_name}")
            

cv.imshow("Detected Shapes", img)
cv.waitKey(0)
cv.destroyAllWindows()