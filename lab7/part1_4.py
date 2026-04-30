import cv2
import numpy as np

def menu():
    print("1. Original")
    print("2. Cut horizontally")
    print("3. Cut Vertically")
    print("4. Divide in an N x N grid")
    print("esc: exit")
    print("select option (press key)")

def resize_image(img, width, height):
    size = (width, height)
    img_resize = cv2.resize(img, size)
    return img_resize

def cut_horizontally(img):
    up = img[0:600, 0:200]
    down = img[0:600, 200:400]
    return (up, down)

def cut_vertically(img):
    left = img[0:300, 0:400]
    right = img[300:600, 0:400]
    return (right, left)

def cut_quadrants(img):
    print("grid size (ex. 2 = 2x2) (press key):")
    n = cv2.waitKey(0) & 0xFF
    n = n - 48
    
    if n <= 0:
        print("Invalid number!")
        return

    img_height, img_width = img.shape[:2]
    
    width_step = img_width / n
    height_step = img_height / n

    window_count = 0
    
    for row in range(n):
        for col in range(n):
            y_start = int(row * height_step)
            y_end = int((row + 1) * height_step)
            
            x_start = int(col * width_step)
            x_end = int((col + 1) * width_step)
            
            img_modified = img[y_start:y_end, x_start:x_end]
            
            cv2.imshow(f"image_{window_count}", img_modified)
            window_count += 1

if __name__ == "__main__":
    img = cv2.imread("watermelon.jpeg")
    
    if img is None:
        print("Error: Image not found.")
        exit()
        
    img = resize_image(img, 400, 600)
    
    while True:
        menu()        
        cv2.imshow("image", img) 
        
        img_modified1 = None
        img_modified2 = None
        key = cv2.waitKey(0) & 0xFF
        
        cv2.destroyAllWindows()
        
        cv2.imshow("image", img) 
        
        match key:
            case 49:
                img_modified1 = resize_image(img, 400, 600)
            case 50:
                img_modified1, img_modified2 = cut_horizontally(img)
            case 51:
                img_modified1, img_modified2 = cut_vertically(img)
            case 52:
                cut_quadrants(img)
            case 27:
                break
                
        if img_modified1 is not None:
            cv2.imshow("image1", img_modified1) 
        if img_modified2 is not None:
            cv2.imshow("image2", img_modified2) 
            
    cv2.destroyAllWindows()