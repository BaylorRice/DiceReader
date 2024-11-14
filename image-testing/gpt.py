from PIL import Image
from pytesseract import pytesseract
import cv2
import numpy as np

# Path to tesseract executable (adjust to your installation)
pytesseract.tesseract_cmd = r'tesseract\tesseract.exe'

# Load the image using OpenCV
image_path = r'image-testing\image.png'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to make the numbers stand out
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imshow("Display window", thresh)
k = cv2.waitKey(0)

# Optionally, use edge detection to isolate the die
edges = cv2.Canny(thresh, 300, 500)
cv2.imshow("Display window", edges)
k = cv2.waitKey(0)

# Crop the image to isolate the top face (manually or via contour detection)
# For simplicity, you can manually set the crop if needed:
#cropped_image = thresh[y1:y2, x1:x2]  # Adjust coordinates accordingly

#rows,cols,channels = image.shape
#for i in range(0,361):
#    M = cv2.getRotationMatrix2D((cols/2,rows/2),i,1) 
#    rotate = cv2.warpAffine(edges,M,(cols,rows))
#    text = pytesseract.image_to_string(rotate, config='--psm 6 digits')
#    print(i, "; Detected number:", text.strip())
#    print("")


# Run pytesseract on the preprocessed image
text = pytesseract.image_to_string(edges, config='--psm 6 digits')
print("Detected number:", text.strip())
