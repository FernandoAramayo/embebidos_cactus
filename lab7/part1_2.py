import cv2

def resize_image(img, option):
    match option:
        case 1:
             return img
        case 2:
            return cv2.resize(img, None, fx=0.5, fy = 0.5)
        case 3:
            return cv2.resize(img, None, fx=1.5, fy = 1.5)
        case 4:
            return cv2.resize(img, None, fx=2.5, fy = 2.5)

def menu():
    print("1. original")
    print("2. small")
    print("3. medium")    
    print("4. big")
    option = int(input("Select option: "))
    return option


if __name__ == "__main__":
    img = cv2.imread("watermelon.jpeg")
    option = menu()
    img_resize = resize_image(img, option)
    cv2.imshow("resized image", img_resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()