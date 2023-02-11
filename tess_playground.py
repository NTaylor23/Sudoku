import cv2
import numpy as np

def blur_and_thresh(img):
    blur = cv2.GaussianBlur(img, (5,5), 0)
    return cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

IN = 'images/big.JPG'

image = cv2.imread(IN)

# make sure to change scaling constants in the actual app
image = cv2.resize(image, None, fx= 0.3, fy= 0.3, interpolation= cv2.INTER_LINEAR)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

h, w, _ = image.shape

processed = blur_and_thresh(gray)
contours, _ = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

max_area = 0

for contour in contours:
    area = cv2.contourArea(contour)
    if area > max_area:
        max_area = area
        best_contour = contour
    
#cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

top_left = top_right = bottom_left = bottom_right = np.float32([0, 0])
min_x, min_y, max_x, max_y = float('inf'), float('inf'), 0, 0

for point in best_contour:
    x, y = int(point[0][0]), int(point[0][1])
    min_y = min(min_y, y)
    max_y = max(max_y, y)

top_left = np.float32([float('inf'), min_y])
top_right = np.float32([0, min_y])
bottom_left = np.float32([float('inf'), max_y])
bottom_right = np.float32([0, max_y])

for point in best_contour:
    x, y = int(point[0][0]), int(point[0][1])
    if y in range(min_y - 10, min_y + 10):
        top_left[0] = min(x, top_left[0])
        top_right[0] = max(x, top_right[0])
        
    elif y in range(max_y - 10, max_y + 10):
        bottom_left[0] = min(x, bottom_left[0])
        bottom_right[0] = max(x, bottom_right[0])

# top left, top right, bottom left, bottom right
corners = np.float32([top_left, top_right, bottom_left, bottom_right])

for x in range(4):
    cv2.circle(processed, (int(corners[x][0]), int(corners[x][1])), 5, (0, 0, 255), -1)

new_corners = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

perspective = cv2.getPerspectiveTransform(corners, new_corners)
P = cv2.warpPerspective(gray, perspective, (w, h))

P = cv2.resize(P, (900, 900))
cv2.imshow("perspective", P)
cv2.imwrite('images/perspective.jpg', P)

cv2.waitKey(0)
cv2.destroyAllWindows