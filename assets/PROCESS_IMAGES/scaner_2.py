import cv2 # opencv-python
import numpy as np
from skimage.filters import threshold_local # scikit-image
import imutils

# read the input image
image = cv2.imread("C:/Users/rachi\Downloads\Snapchat-560386619.jpg")

# clone the original image
original_image = image.copy()
# resize using ratio (old height to the new height)
ratio = image.shape[0] / 500.0
image = imutils.resize(image, height=500)





#  change the color space to YUV
image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)

# grap only the Y component
image_y = np.zeros(image_yuv.shape[0:2], np.uint8)
image_y[:, :] = image_yuv[:, :, 0]

# blur the image to reduce high frequency noises
image_blurred = cv2.GaussianBlur(image_y, (3, 3), 0)
#image_blurred=cv2.threshold(image_blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# find edges in the image
edges = cv2.Canny(image_blurred, 50, 200, apertureSize=3)

# show the original image and the edge detected image
print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()



edged=edges



#find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break
# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()



def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped







#get the contours of the largest polygon in the image


cropped_image = four_point_transform(original_image, screenCnt.reshape(4, 2) * ratio)

# check if the polygon has four point


#Binarize the cropped image
gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

T = threshold_local(gray_image, 11, offset=10, method="gaussian")
binarized_image = (gray_image > T).astype("uint8") * 255

# Show images
cv2.imshow("Original", imutils.resize(original_image,height = 650))
cv2.imshow("Scanned", imutils.resize(binarized_image,height = 650))
cv2.imshow("Cropped", imutils.resize(cropped_image,height = 650))
cv2.waitKey(0)

