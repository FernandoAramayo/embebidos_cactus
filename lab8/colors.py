import cv2
import numpy as np

def get_colors(color_list):
    red1_lower = np.array([0, 50, 50])
    red1_upper = np.array([10, 255, 255])
    red2_lower = np.array([170, 50, 50])
    red2_upper = np.array([180, 255, 255])
    green_lower = np.array([36, 50, 50])
    green_upper = np.array([89, 255, 255])
    blue_lower = np.array([90, 50, 50])
    blue_upper = np.array([130, 255, 255])
    orange_lower = np.array([10, 100, 20])
    orange_upper = np.array([25, 255, 255])

    all_colors = [
        {"name": "red", "lower": red1_lower, "upper": red1_upper},
        {"name": "red", "lower": red2_lower, "upper": red2_upper},
        {"name": "green", "lower": green_lower, "upper": green_upper},
        {"name": "blue", "lower": blue_lower, "upper": blue_upper},
        {"name": "orange", "lower": orange_lower, "upper": orange_upper}
    ]

    desired_colors = [color for color in all_colors if color["name"] in color_list]
    return desired_colors


def color_mask(img, *color_list):
    colors = get_colors(color_list)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_modified = np.zeros_like(img)
    for color in colors:
        mask = cv2.inRange(img_hsv, color["lower"], color["upper"])
        img_color = cv2.bitwise_and(img, img, mask=mask)
        img_modified = cv2.bitwise_or(img_modified, img_color)
    return img_modified

        

if __name__ == "__main__":
    img1 = cv2.imread("cardinal.jpeg")
    filtered_img1 = color_mask(img1, "orange")
    cv2.imshow("filtered_cardinal", filtered_img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()