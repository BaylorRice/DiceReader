from PIL import Image
import os
"""
This gets the images out of the d6_pics_2/originals folder and then 
rotates each one by 5 degrees from 0-355 degrees for each image in order 
to add more variability in my dataset, I performed the same thing for the 
number_dataset but with 15 degree intervals 
"""
source_dir = 'd6_pics_2/originals'  
output_dir = 'd6_pics_2/augmented'
os.makedirs(output_dir, exist_ok=True)

angles = list(range(0,356,15))

for filename in os.listdir(source_dir):
    if filename.lower().endswith('.jpg'):
        num_label = os.path.splitext(filename)[0]  
        img_path = os.path.join(source_dir, filename)
        img = Image.open(img_path)
        for angle in angles:
            rotated = img.rotate(angle, expand=True)
            new_filename = f"{num_label}_{angle}.jpg"
            rotated.save(os.path.join(output_dir, new_filename))





