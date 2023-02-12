from draw_answer import *
from ocr import *
from process_image import *
from solve import *
from webcam import *

WC = Webcam()

if __name__ == '__main__':
    contour, frame = WC.get_puzzle_area()
    PI = ProcessImage(contour, frame)
    cropped = PI.warp_perspective()
    
    # cv2.imshow('Cropped', cropped)
    # cv2.waitKey(0)
    # cv2.destroyWindow('Cropped')
    # print('Reading...')
    ocr = OCR(cropped)
    
    grid = ocr.read_numbers()
    original_state = grid.copy()
    print(grid)
    # cont = input("Continue?\n")
    cont = 'y'
    if cont == 'y':
        solver = Solver(grid)
        res = solver.start()
 
    DA = DrawAnswer(cropped, original_state, res)
    DA.create_image()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    