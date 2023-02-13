from PIL import Image
from string import digits

from tesserocr import PyTessBaseAPI
import cv2
import numpy as np

from traceback import format_exc

class OCR:
    
    def __init__(self, img) -> None:
        self.img = cv2.resize(img, (900, 900))
        self.original_state = [[0 for _ in range(9)] for _ in range(9)]
        self.grid = np.zeros((9, 9), dtype=np.uint8)
        self.tess_path = '/usr/local/Cellar/tesseract/5.2.0/share/tessdata/.'
    
    def read_numbers(self):
        blurred = cv2.blur(self.img, (1, 1))
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        threshed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
        cv2.imshow('threshed', threshed)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        with PyTessBaseAPI(lang='eng', path=self.tess_path, psm=10) as api:
            api.SetVariable('tessedit_char_whitelist', digits)
            for row in range(9):
                r = []
                for col in range(9):
                    square = threshed[10 + row * 100:(row + 1) * 100 - 10, 10 + col * 100:(col + 1) * 100 - 10]
                    img = Image.fromarray(np.uint8(square))
                    api.SetImage(img)
                    txt = api.GetUTF8Text()
                    if txt:
                        self.grid[row, col] = txt[0]
                self.original_state.append(r)
        
        return self.grid
        
            
        
        