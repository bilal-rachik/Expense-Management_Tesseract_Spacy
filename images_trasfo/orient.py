import cv2
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def image_to_text(image):
    rot_data = pytesseract.image_to_osd(image)
    print("[OSD] " + rot_data)
    rot = re.search('(?<=Rotate: )\d+', rot_data).group(0)
    angle = float(rot)
    if angle > 0:
        angle = 360 - angle
    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    config = ('--oem 1')
    text = pytesseract.image_to_string(rotated, lang='fra+eng',config=config)
    return text


