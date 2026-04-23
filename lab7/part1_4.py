import cv2
import numpy as np

def menu():
    print("1. Original")
    print("2. Cut horizontally")
    print("3. Cut Vertically")
    print("4. Divide in N cuadrants")
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
    print("pres key of number of cuadrants: ")
    n = cv2.waitKey(0) & 0xFF
    n = n-48
    width = 400/n
    height = 600/n

    current_width = 0
    current_height = 0
    for i in range(n):
        height_limit = int(current_height+height)
        width_limit = int(current_width+width)
        img_modified = img[current_height:height_limit, current_width:width_limit]
        current_height=height_limit
        current_width=width_limit
        cv2.imshow(f"image{i}", img_modified)

if __name__ == "__main__":
    img = cv2.imread("watermelon.jpeg")
    img = resize_image(img, 400,600)
    cv2.imshow("image", img)
    while True:
        menu()
        img_modified1 = None
        img_modified2 = None
        key = cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
        cv2.imshow("image", img)
        
        match key:
            case 49:
                img_modified1 = resize_image(img, 400,600)
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