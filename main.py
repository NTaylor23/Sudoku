from ocr import *
from process_image import *
from solve import *
from webcam import *

WC = Webcam()

if __name__ == '__main__':
    contour, frame = WC.get_puzzle_area()
    PI = ProcessImage(contour, frame)
    cropped = PI.warp_perspective()
    print(cropped.shape)
    cv2.imshow('cropped', cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print('Reading...')
    ocr = OCR(cropped)
    grid = ocr.read_numbers()
    print(grid)
    cont = input("Continue?")
    if cont == 'y':
        solver = Solver(grid)
        res = solver.start()
        print(res)
        
        
    