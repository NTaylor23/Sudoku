import cv2

def show_image(image, name='image', debug=False):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()