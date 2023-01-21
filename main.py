from PIL import Image, ImageFont, ImageDraw

import cv2
import numpy as np
import pytesseract as pt
import traceback

IN_PATH = 'images/easy.png'
OUT_PATH = 'images/sample.jpeg'

grid: np.array = np.zeros((9, 9), dtype=np.uint8)
original_state = []

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

def solve():
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
    
def create_image(solved):
    try:
        out = Image.open(IN_PATH)
        w, h = out.size
        sub_w, sub_h = w // 9, h // 9
        print(sub_w, sub_h)
        # get a drawing context
        d = ImageDraw.Draw(out)

        for y in range(9):
            for x in range(9):
                if original_state[y][x] == '':
                    d.multiline_text(((sub_w * x) + sub_w // 2, (sub_h * y) + sub_h // 2), str(solved[y][x]), fill=(0, 0, 0))
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
                num = pt.image_to_string(img[10 + row * 100:(row + 1) * 100 - 10, 10 + col * 100:(col + 1) * 100 - 10, :], 
                                         config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789')
                if num:
                    grid[row, col] = num
                r.append(num)
            original_state.append(r)
    except Exception as e:
        print(e)
        
    print('Solved:')
    solve()

    
main()
