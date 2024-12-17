import os
import glob
import cv2
import supervision as sv
from inference import get_model
"""
This gets all of the images in d6_pics_2/augmented and runs them 
through the roboflow model and gets all of the coordinates for the 
bounding box for each image, and then creates a .txt file in d6_pics_2/labels 
under the same name as its equivalant .jpg file
"""

os.environ["ROBOFLOW_API_KEY"] = "J9tV3kwjI7eWiwKtmw4h"
model = get_model(model_id="dice-finder-qey6z/1")

image_folder = "d6_pics_2/augmented"
labels_folder = "d6_pics_2/labels"
os.makedirs(labels_folder, exist_ok=True)

# this gets a list of all jpg images in the augmented folder
image_paths = glob.glob(os.path.join(image_folder, "*.jpg"))

for img_path in image_paths:
    image = cv2.imread(img_path)
    if image is None:
        print(f"Warning: Could not load image {img_path}")
        continue
    
    cropped = image[0:2592, 350:3600]

    # this runs the inference
    results = model.infer(cropped)[0]
    
    base_name = os.path.splitext(os.path.basename(img_path))[0]
    txt_path = os.path.join(labels_folder, f"{base_name}.txt")
    
    """
    this writes the bounding box coordinates (x, y, width, height) to a .txt file
    results.predictions is a list of ObjectDetectionPrediction objects
    which contain x, y, width, and height
    """
    
    with open(txt_path, "w") as f:
        for pred in results.predictions:
            x = pred.x
            y = pred.y
            w = pred.width
            h = pred.height
            f.write(f"{x} {y} {w} {h}\n")
    
    print(f"Processed {img_path} and saved bounding boxes (x, y, width, height) to {txt_path}")

print("All images processed.")
