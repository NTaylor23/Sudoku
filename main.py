from draw_answer import *
from ocr import *
from process_image import *
from solve import *
from util import show_image
from webcam import *

WC = Webcam()

if __name__ == '__main__':
    contour, frame = WC.get_puzzle_area()
    PI = ProcessImage(contour, frame)
    processed, cropped = PI.warp_perspective()
    print('Cropped dimensions:', cropped.shape)
    # show_image(cropped, 'Cropped')
    print('Reading...')
    ocr = OCR(processed)
    
    grid = ocr.read_numbers()
    original_state = grid.copy()
    print(grid)
    #cont = input("Continue?\n")
    cont = 'y'
    if cont == 'y':
        solver = Solver(grid)
        res = solver.start()
    
        if res is not None:
            DA = DrawAnswer(cropped, original_state, res)
            DA.create_image()
        else:
            print('Cannot solve: invalid board')
    else:
        print('Terminating...')