import cv2
import numpy as np
import pytesseract as pt
from traceback import format_exc

class OCR:
    def __init__(self, img) -> None:
        self.img = cv2.resize(img, (900, 900))
        self.original_state = [[0 for _ in range(9)] for _ in range(9)]
        self.grid = np.zeros((9, 9), dtype=np.uint8)
    
    def read_numbers(self):
        blurred = cv2.blur(self.img, (5, 5))
        (T, threshed) = cv2.threshold(blurred, 122, 255, cv2.THRESH_BINARY)
        try:
            for row in range(9):
                r = []
                for col in range(9):
                    # traverse the image square by square, and do OCR on each square
                    # this is quite slow, and needs to be optimized - current runtime about 3s
                    num = pt.image_to_string(threshed[10 + row * 100:(row + 1) * 100 - 10, 10 + col * 100:(col + 1) * 100 - 10, :], 
                                            config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789')
                    if num:
                        self.grid[row, col] = num
                    r.append(num)
                self.original_state.append(r)
        except Exception as e:
            print(e, format_exc())
            
        return self.grid
        
            
        
        