import cv2
import numpy as np

# Load the image
image_path = r'image-testing\image.jpg'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to create a binary image
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort contours by area (largest first)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# Loop over contours to find the best candidate for the dice face
for contour in contours:
    # Get the bounding rectangle for the contour
    x, y, w, h = cv2.boundingRect(contour)
    
    # Optionally, apply a size filter to exclude small areas
    if w > 50 and h > 50:  # Adjust the size filter as needed
        cropped_image = image[y:y+h, x:x+w]
        cv2.imshow('Cropped Dice Face', cropped_image)
        cv2.waitKey(0)  # Wait for key press to display the image
        cv2.destroyAllWindows()
        break  # Stop after finding the largest valid contour

# Save or pass the cropped image for further processing (e.g., OCR)
cv2.imwrite('cropped_dice_face.jpg', cropped_image)
cv2.imshow('Cropped Dice Face', cropped_image)
cv2.waitKey(0)
