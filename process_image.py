import cv2
import numpy as np

class ProcessImage:
    def __init__(self, contour, frame) -> None:
        self.frame = frame
        self.contour = contour
        self.h, self.w, self._ = frame.shape
        self.top_left = self.top_right = self.bottom_left = self.bottom_right = np.float32([0, 0])
        self.original_dimensions = np.float32([[0, 0], [self.w, 0], [0, self.h], [self.w, self.h]])

    def warp_perspective(self):
        # Approximate the contour with a polygonal curve 
        approx = cv2.approxPolyDP(self.contour, 0.05 * cv2.arcLength(self.contour, True), True)
        
        # If the curve has four corners...
        if len(approx) == 4:
            
            puzzle_corners = [None] * 4            
            for i in range(4):
                puzzle_corners[i] = tuple(approx[i][0])
            
            # Sort all points by increasing Y value
            puzzle_corners = sorted(puzzle_corners, key=lambda y: y[1])
            
            # Sort top points and bottom points by increasing X value
            top = sorted(puzzle_corners[:2], key=lambda x: x[0])
            bottom = sorted(puzzle_corners[2:], key=lambda x: x[0])
            
            # Merge points into numpy array
            puzzle_corners = np.array(top + bottom, dtype=np.float32)
            
        perspective = cv2.getPerspectiveTransform(puzzle_corners, self.original_dimensions)
        cropped = cv2.warpPerspective(self.frame, perspective, (self.w, self.h))
        return cv2.resize(cropped, (900, 900))
        