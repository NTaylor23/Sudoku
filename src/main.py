from PIL import Image, ImageFont, ImageDraw

import cv2
import numpy as np
import pytesseract as pt
import traceback

IN_PATH = 'images/easy.png'
OUT_PATH = 'images/sample.jpeg'

# numpy array to read the interpreted digits from the input image
grid: np.array = np.zeros((9, 9), dtype=np.uint8)

# python list to hold the interpreted digits for reference when the solved image is created
original_state = []

# check each row, column and 3x3 square for the current number n
# this is done each iteration during the backtracking algorithm
def possible(y: int, x: int, n: int) -> bool:
    global grid
    
    # check horizontal
    for i in range(0, 9):
        if grid[y][i] == n:
            return False
    
    # check vertical
    for i in range(0, 9):
        if grid[i][x] == n:
            return False
    
    _y = y - (y % 3)
    _x = x - (x % 3)
    
    # check square
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[_y + i][_x + j] == n:
                return False
                     
    return True

# recursive backtracking
def solve() -> None:
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    create_image(grid)


def create_image(solved) -> None:
    try:
        # configure image for output
        out = Image.open(IN_PATH)
        w, h = out.size
        # image should technically be a square, this is for simplicity
        sub_w, sub_h = w // 9, h // 9

        # image setup
        d = ImageDraw.Draw(out)
        ft = ImageFont.truetype("assets/GothamMedium.ttf", 24)
        
        for y in range(9):
            for x in range(9):
                if original_state[y][x] == '':
                    # add text on squares where no information was present in the original image
                    d.text(((sub_w * x) + sub_w // 2, (sub_h * y) + sub_h // 2), str(solved[y][x]), font=ft, fill=(255, 0, 0))
        out.show()
        
    except Exception as e:
        print(e, traceback.format_exc())
    

def main() -> None:
    
    try:
        img = cv2.imread(IN_PATH)
        img = cv2.resize(img, (900, 900))
        
        for row in range(9):
            r = []
            for col in range(9):
                # traverse the image square by square, and do OCR on each square
                # this is quite slow, and needs to be optimized - current runtime about 3s
                num = pt.image_to_string(img[10 + row * 100:(row + 1) * 100 - 10, 10 + col * 100:(col + 1) * 100 - 10, :], 
                                         config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789')
                if num:
                    grid[row, col] = num
                r.append(num)
            original_state.append(r)
    except Exception as e:
        print(e)
        
    solve()
    
main()
