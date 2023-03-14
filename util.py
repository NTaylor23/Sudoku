import cv2

def show_image(image, name='image'):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def print_confidence_values(confidence_values):
    print('[Numeric Value : Confidence Rating From Tesseract')
    for line in confidence_values:
        for tup in line:
            val, conf = tup
            print(f'{val}: {str(round(float(conf / 100), 3)).ljust(4)}  ', end='')
        print('\n\n')