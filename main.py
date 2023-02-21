import sys

from draw_answer import *
from ocr import *
from process_image import *
from solve import *
from util import show_image, print_confidence_values
from webcam import *

WC = Webcam()

if __name__ == '__main__':
    
    debug = len(sys.argv) == 2 and sys.argv[1] == '-d'
    
    # Get contour and image of puzzle from webcam
    contour, frame = WC.get_puzzle_area()
    
    # Crop and convert image to a format suitable for OCR
    PI = ProcessImage(contour, frame)
    processed, cropped = PI.warp_perspective()
    
    if debug:
        print('Press [ESC] to continue.')
        show_image(cropped, 'Cropped')
        
    print('Reading...')
    
    # Analyze numbers on puzzle and save the original state
    ocr = OCR(processed, debug)
    grid = ocr.read_numbers()
    original_state = grid.copy()
    
    # print(grid)
    if debug:
        print(grid)
        #print_confidence_values(confidence)
        pass
    
    cont = 'y'
    if debug:
        cont = input('Press [y] to continue or [x] to cancel:\n')
        
    # Solve puzzle
    if cont == 'y':
        solver = Solver(grid)
        res = solver.start()

        if res is not None:
            # Draw the solved puzzle onto the original image
            DA = DrawAnswer(cropped, original_state, res)
            DA.create_image()
        else:
            # OCR mistakes were made...
            print('Cannot solve: invalid board')
    else:
        print('Exiting.')
