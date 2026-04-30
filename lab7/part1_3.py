import cv2

if __name__ == "__main__":
    img = cv2.imread("watermelon.jpeg")
    cv2.imshow("image", img)
    print("press esc to exit")
    while True:
        key = cv2.waitKey(0) & 0xFF
        
        if key == 27:
            break
        else:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            cv2.imshow("image", img)
    cv2.destroyAllWindows()