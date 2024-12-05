import cv2
import numpy as np

image1 = cv2.imread("motion-testing/image1.jpg")
image2 = cv2.imread("motion-testing/image2.jpg")
diff = cv2.absdiff(image1, image2)
cv2.imwrite("motion-testing/diff.png", diff)
mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
cv2.imwrite("motion-testing/mask.png", mask)

th = 1
imask = mask>th

canvas = np.zeros_like(image2,np.uint8)
canvas[imask] = image2[imask]

cv2.imwrite("motion-testing/result.png", canvas)