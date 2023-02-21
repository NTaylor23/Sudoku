from PIL import Image
from string import digits
from tesserocr import PyTessBaseAPI
from util import show_image

import cv2
import numpy as np

class OCR:
    
    def __init__(self, img) -> None:
        self.img = img
        self.original_state = [[0 for _ in range(9)] for _ in range(9)]
        self.grid = np.zeros((9, 9), dtype=np.uint8)
    
    def read_numbers(self):
        
        show_image('what the ocr sees', self.img)

        with PyTessBaseAPI(lang='eng', psm=10) as api:
            api.SetVariable('tessedit_char_whitelist', digits[1:])
            for row in range(9) :
                r = []
                for col in range(9):
                    square = self.img[10 + row * 100:(row + 1) * 100 - 10, 10 + col * 100:(col + 1) * 100 - 10]
                    img = Image.fromarray(np.uint8(square))
                    api.SetImage(img)
                    txt = api.GetUTF8Text().replace('\n', '')
                    if txt:
                        self.grid[row, col] = int(txt)
                self.original_state.append(r)
        
        return self.grid
        
            
        
        