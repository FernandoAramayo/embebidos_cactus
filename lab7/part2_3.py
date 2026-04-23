import cv2

class Image:
    def __init__(self, img, current_scale="BGR"):
        self.img = img
        self.current_scale = current_scale

    def to_gray(self):
        self.img_modified = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def to_hsv(self):
        self.img_modified = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

    def to_bgr(self):
        self.img_modified = self.img

def menu():
    print("1. RGB")
    print("2. Grayscale")
    print("3. HSV")
    print("esc: exit")
    print("select option (press key)")

if __name__ == "__main__":
    image = cv2.imread("watermelon.jpeg")
    image_ob = Image(image)
    cv2.imshow("image", image_ob.img)
    print("press esc to exit")
    while True:
        menu()
        key = cv2.waitKey(0) & 0xFF
        
        match key:
            case 49:
                image_ob.to_bgr()
            case 50:
                image_ob.to_gray()
            case 51:
                image_ob.to_hsv()
            case 27:
                break
        cv2.destroyAllWindows()
        cv2.imshow("image", image_ob.img_modified)
