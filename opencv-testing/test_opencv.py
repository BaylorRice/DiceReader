import cv2 as cv
import sys

img = cv.imread("opencv-testing\image.jpg", cv.IMREAD_GRAYSCALE)

if img is None:
    sys.exit("Could not read the image")

cv.imshow("Display Window", img)
h, w = img.shape[:2]
print("Height = {}, Width = {}".format(h, w))
k = cv.waitKey(0)