import cv2
import pytesseract
import urllib
import numpy as np
import re

# Installs: https://www.learnopencv.com/deep-learning-based-text-recognition-ocr-using-tesseract-and-opencv/

if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Uncomment the line below to provide path to tesseract manually
    # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

    # Read image from URL


    image=cv2.imread('C:/Users/rachi/Downloads/opt/ndf/F18557244860C4F9EE590FEF2336FFB7n.jpg')
    cv2.imshow('sample image', image)

    cv2.waitKey(0)  # waits until a key is pressed
    cv2.destroyAllWindows()  # destroys the window showing image


    # decode as color

    #  TAKEN FROM: https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    rot_data = pytesseract.image_to_osd(image);
    print("[OSD] " + rot_data)
    rot = re.search('(?<=Rotate: )\d+', rot_data).group(0)

    angle = float(rot)
    if angle > 0:
        angle = 360 - angle
    print("[ANGLE] " + str(angle))

    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    ##  TODO: Rotated image can be saved here
    print(pytesseract.image_to_osd(rotated));
    print("[TEXT]")
    # Run tesseract OCR on image
    config = ('--oem 1 --psm 6')
    text = pytesseract.image_to_string(rotated, lang='eng', config=config)

    print(text)

    # Print recognized text
    #print(text.encode(encoding='UTF-8'))
