import os
import glob
import shutil

'''
This code seperates the cropped images from the folder "d6_pics_2/cropped" 
and puts it into 1-6 class subdirectories of "number_dataset
'''
source_dir = "d6_pics_2/cropped"
target_dir = "number_dataset"


classes = ['1', '2', '3', '4', '5', '6']
for c in classes:
    class_path = os.path.join(target_dir, c)
    os.makedirs(class_path, exist_ok=True)

image_paths = glob.glob(os.path.join(source_dir, "*.jpg"))

for img_path in image_paths:
    filename = os.path.basename(img_path)
    
    # this thing splits by underscore to identify class
    # "1_4_15_0.jpg" -> class "1"
    class_name = filename.split('_')[0]
    
    # destination
    dest_path = os.path.join(target_dir, class_name, filename)
    shutil.copy2(img_path, dest_path)

print("Copying completed!")
