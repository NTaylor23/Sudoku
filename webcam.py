import cv2
import numpy as np
from util import show_image

class Webcam:
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)
        self.best_frame = None 
        self.final_contour = None

    def read_frame(self, image: np.ndarray) -> bool:
        """ Process an image frame and attempt to locate a square representing a Sudoku board.
        This is implemented by finding the largest contiguous square in the frame and calculating its area.

        Args:
            image (np.ndarray): The current image frame.
            
        Returns:
            bool: True if a viable candidate is found, False otherwise.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 50, 50)
        contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        max_area = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                best_contour = contour
                approx = cv2.approxPolyDP(best_contour, 0.01 * cv2.arcLength(best_contour, True), True)
                
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(best_contour)
                    ratio = float(w) / h
                    
                    if (ratio >= 0.96 and ratio <= 1.1) and w * h > 100000:
                        self.final_contour = best_contour
                        return True
                    
                    cv2.drawContours(image, best_contour, -1, (0, 0, 255), 4)
                    
        cv2.imshow("webcam", image)

    def get_puzzle_area(self) -> tuple:
        """ Read webcam input frame by frame until a Sudoku board is found.

        Returns:
            tuple: (Board contour, frame containing best image of board)
        """
        
        while True:
            _, frame = self.cap.read()
                
            if self.read_frame(frame):
                self.best_frame = frame
                break
            
            if cv2.waitKey(1) & 0xFF ==ord("q"):
                break

        self.cap.release()
        
        # debug
        frame_copy = self.best_frame.copy()
        cv2.drawContours(frame_copy, self.final_contour, -1, (0, 225, 0), 4)
        show_image(frame_copy, 'Best Frame')
        print('Best frame dimensions:', self.best_frame.shape)
        # /debug
        
        return (self.final_contour, self.best_frame)
            
        
if __name__ == '__main__':
    W = Webcam()
    W.get_puzzle_area()