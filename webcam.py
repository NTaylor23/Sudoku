import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

winner = None 

def blur_and_thresh(img):
    blur = cv2.GaussianBlur(img, (5,5), 0)
    return cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

def read(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    processed = blur_and_thresh(gray)
    contours, _ = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    max_area = 0
    flag = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            best_contour = contour
            approx = cv2.approxPolyDP(best_contour, 0.01 * cv2.arcLength(best_contour, True), True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(best_contour)
                
                ratio = float(w) / h
                
                if ratio >= 0.97 and w * h > 100000:
                    return True
                # print(w, h, ratio)

                    
                
    image = cv2.drawContours(image, best_contour, -1, (0, 255, 0), 4)
    cv2.imshow("webcam", image)

while True:
    _, frame = cap.read()
    
    if read(frame):
        winner = frame
        break
    
    key = cv2.waitKey(5)
    
    if key == 27:
        break
cap.release()

cv2.imshow('Best frame', winner)
cv2.waitKey(0)
cv2.destroyAllWindows()

