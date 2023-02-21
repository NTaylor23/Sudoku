import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import traceback

class DrawAnswer:
    def __init__(self, img, original_state, answer) -> None:
        self.img = img
        self.original_state = original_state
        self.answer = answer
        
    def create_image(self) -> None:
        try:
            # configure image for output
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGBA)
            out = Image.fromarray(self.img)
            w, h = 900, 900
            sub_w, sub_h = 100, 100

            # image setup
            d = ImageDraw.Draw(out)
            ft = ImageFont.truetype("assets/GothamMedium.ttf", 48)
            
            for y in range(9):
                for x in range(9):
                    if self.original_state[y][x] == 0:
                        d.text(((sub_w * x) + sub_w // 2, (sub_h * y) + sub_h // 2), str(self.answer[y][x]), font=ft, fill=(0, 0, 0))
                        
            result = cv2.cvtColor(np.array(out), cv2.COLOR_RGB2BGR)
            result = cv2.resize(result, (400, 400))
            print('Complete.')
            cv2.destroyAllWindows()
            cv2.imshow("Result", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            
        except Exception as e:
            print(e, traceback.format_exc())