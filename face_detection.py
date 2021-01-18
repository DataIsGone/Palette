# plot photo with detected faces using opencv cascade classifier
import cv2
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import ytimg
from cv2 import imread
from cv2 import imshow
from cv2 import imwrite
from cv2 import waitKey
from cv2 import destroyAllWindows
from cv2 import CascadeClassifier
from cv2 import rectangle

# Credit: Nalin Chhibber (https://nalinc.github.io/blog/2018/skin-detection-python-opencv/)
min_HSV = np.array([0, 58, 30], dtype = "uint8")
max_HSV = np.array([33, 255, 255], dtype = "uint8")
# max_HSV = np.array([233, 223, 222], dtype = "uint8")

# grab just the face
def get_face(pixels):
    # load the pre-trained model
    classifier = CascadeClassifier('haarcascade_frontalface_default.xml')

    # perform face detection
    facebox = classifier.detectMultiScale(pixels)
    print(type(facebox))
    print(facebox)
    print()

    x, y, width, height = facebox[0]
    crop_x, crop_y = x + width, y + height

    facebox_width = facebox[0][2]
    facebox_height = facebox[0][3]

    # crop to face
    crop_face = pixels[y:crop_y, x:crop_x]
    return crop_face    # numpy.ndarray


# select a pixel from the face
def get_avg_color(head_crop):
    """ convert from RGB to HSV, better for skin tones
        Credit: Nalin Chhibber (https://nalinc.github.io/blog/2018/skin-detection-python-opencv/)
    """

    # segment skin from cropped head image
    image_HSV = cv2.cvtColor(head_crop, cv2.COLOR_BGR2HSV)
    skin_region_HSV = cv2.inRange(image_HSV, min_HSV, max_HSV)
    skin_HSV = cv2.bitwise_and(head_crop, head_crop, mask = skin_region_HSV)

    #cv2.imshow('skin tone only', skin_HSV)
    #cv2.waitKey(0)

    # convert back to rgb
    skin_BRG = cv2.cvtColor(skin_HSV, cv2.COLOR_HSV2BGR)

    # calculate average skin tone
    pixel_count = 0
    avg_b = 0
    avg_g = 0
    avg_r = 0
    for pixel in skin_BRG:
        for color in pixel:
            if str(color) != "[0 0 0]":     # b, g, r
                avg_b += color[0]
                avg_g += color[1]
                avg_r += color[2]
                pixel_count += 1
    avg_b = avg_b // pixel_count
    avg_g = avg_g // pixel_count
    avg_r = avg_r // pixel_count
    avg_color = (avg_r, avg_g, avg_b)       # switch from brg to rgb format
    avg_color_bgr = (avg_b, avg_g, avg_r)
    print(avg_color)
    return (avg_color, avg_color_bgr)

def url_to_cv2(url_str):
    resp = urllib.request.urlopen(url_str)
    url_img = np.asarray(bytearray(resp.read()), dtype="uint8")
    url_img = cv2.imdecode(url_img, cv2.IMREAD_COLOR)
    return url_img

def read_from_upload(filename):
    uploaded_img = cv2.imread(filename)
    return uploaded_img

def main():
#     # # test
#     # filename = 'TestImages/test_ryan.jpg'
    filename = 'TestImages/Passed/10.jpeg'
    test_head_crop = get_face(read_from_upload(filename))
    # cv2.imshow('test head crop', test_head_crop)
    # cv2.waitKey(0)
    get_avg_color(test_head_crop)


if __name__ == "__main__":
    main()