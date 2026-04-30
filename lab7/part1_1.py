import cv2

def resize_image(img, width, height):
    size = (width, height)
    img_resize = cv2.resize(img, size)
    return img_resize


if __name__ == "__main__":
    img = cv2.imread("watermelon.jpeg")
    img_resize = resize_image(img, 1000, 1000)
    cv2.imshow("resized image", img_resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()