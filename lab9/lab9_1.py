import cv2

# Initialize the subtractors
mog2 = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
knn = cv2.createBackgroundSubtractorKNN(detectShadows=True)

cap = cv2.VideoCapture('bouncing.mp4.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply subtractors
    mask_mog2 = mog2.apply(frame)
    mask_knn = knn.apply(frame)

    # Thresholding to remove shadows (shadows are usually gray/127 in the mask)
    _, mask_mog2_bin = cv2.threshold(mask_mog2, 250, 255, cv2.THRESH_BINARY)
    _, mask_knn_bin = cv2.threshold(mask_knn, 250, 255, cv2.THRESH_BINARY)

    cv2.imshow('Original', frame)
    cv2.imshow('MOG2 Mask', mask_mog2_bin)
    cv2.imshow('KNN Mask', mask_knn_bin)

    if cv2.waitKey(27) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()