import cv2

def to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

if __name__ == "__main__":
    img = cv2.imread("watermelon.jpeg")
    img_gray = to_grayscale(img)
    cv2.imshow("gryascale", img_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
