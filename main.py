from solve import *
from webcam import *

WC = Webcam()

if __name__ == '__main__':
    contour, frame = WC.get_puzzle_area()
    