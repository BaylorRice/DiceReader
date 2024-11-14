from pytesseract import pytesseract as pyt
from PIL import Image

path = r"tesseract\tesseract.exe"
image_path = r"image-testing\image.jpg"

img = Image.open(image_path)

pyt.tesseract_cmd = path
text = pyt.image_to_bo(img)

print(text)