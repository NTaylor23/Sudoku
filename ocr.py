from PIL import Image
from string import digits
from tesserocr import PyTessBaseAPI
from util import show_image

import cv2
import numpy as np

class OCR:
    
    def __init__(self, img, debug=False) -> None:
        self.img = img
        self.grid = np.zeros((9, 9), dtype=np.uint8)
        self.debug = debug
        
    def get_most_frequent_element(self, number_string):
        indices, max, choice = [0] * 10, 0, 0
        
        for num in number_string:
            indices[int(num)] += 1
            
        for idx, count in enumerate(indices):
            if count > max:
                max = count
                choice = idx
                
        return choice
        
    def reassess_number(self, img):
        
        with PyTessBaseAPI(lang='eng', psm=7) as api:
            api.SetVariable('tessedit_char_whitelist', digits[1:])
            
            cropped = img.crop((10, 0, img.size[0] - 10, img.size[1]))
            w, h = cropped.size
            adapted_width = w * 5
            new_image = Image.new('L', (adapted_width, h))
            
            x_offset = 0
            for _ in range(0, adapted_width, w):
                new_image.paste(cropped, (x_offset, 0))
                x_offset += w
                
            new_image.show()
            api.SetImage(new_image)
            string = api.GetUTF8Text().strip()
            return self.get_most_frequent_element(string)
    
    def read_numbers(self):
        
        if self.debug:
            show_image(self.img, 'Binary Thresh')
            
        border_size = 10
        square_size = 100
            
        with PyTessBaseAPI(lang='eng', psm=10) as api:
            
            api.SetVariable('tessedit_char_whitelist', digits[1:])
            
            for row in range(9) :
                for col in range(9):
                    # square = self.img[10 + row * 100:(row + 1) * 100 - 10, 10 + col * 100:(col + 1) * 100 - 10]
                    
                    row_start = border_size + row * square_size
                    row_end = (row + 1) * square_size - border_size
                    col_start = border_size + col * square_size
                    col_end = (col + 1) * square_size - border_size

                    square = self.img[row_start : row_end, col_start : col_end]
                    
                    img = Image.fromarray(np.uint8(square))
                    api.SetImage(img)
                    
                    conf = api.MeanTextConf()
                    ocr_result = api.GetUTF8Text().replace('\n', '')
                    
                    if ocr_result:
                        #img.show()
                        number = int(ocr_result)
                        if 0 < conf <= 80:
                            if self.debug:
                                print(f'[{row}, {col}]: {number}')
                            number = self.reassess_number(img)
                        self.grid[row, col] = number
        
        return self.grid
        
            
        
        