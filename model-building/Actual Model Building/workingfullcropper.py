import cv2
from inference import get_model
import supervision as sv
import os
"""
This gets the images from the augmented folder in d6_pics_2 and the 
dimmensions of all of the bounding boxes from the labels directory 
in the d6_pics_2 folder and then iterates over every single image 
and crops them and puts them into the folder d6_pics_2/cropped 

"""

base_dir = "d6_pics_2"
augmented_dir = os.path.join(base_dir, "augmented")
labels_dir = os.path.join(base_dir, "labels")
cropped_dir = os.path.join(base_dir, "cropped")

os.environ["ROBOFLOW_API_KEY"] = "J9tV3kwjI7eWiwKtmw4h"
model = get_model(model_id="dice-finder-qey6z/1")
for filename in os.listdir(augmented_dir):
    if filename.lower().endswith(".jpg"):
        image_path = os.path.join(augmented_dir, filename)
        base_name = os.path.splitext(filename)[0]
        label_path = os.path.join(labels_dir, base_name + ".txt")
        if not os.path.exists(label_path):
            continue
        with open(label_path, 'r') as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            data = line.strip().split()
            if len(data) != 4:
                print(f"Invalid label format in {label_path}: {line}")
                continue
        results = model.infer(image_path)[0]
        pred = results.predictions[0]
        x_center = pred.x
        y_center = pred.y
        width = pred.width
        height = pred.height

        x_min = int(x_center - width/2)
        x_max = int(x_center + width/2)
        y_min = int(y_center - height/2)
        y_max = int(y_center + height/2)

        detections = sv.Detections.from_inference(results)
        bounding_box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()
        image = cv2.imread(image_path)
        cropped = image[y_min:y_max, x_min:x_max]
        out_filename = f"{base_name}_{idx}.jpg"
        out_path = os.path.join(cropped_dir, out_filename)
        cv2.imwrite(out_path, cropped)
        print(f"Cropped image saved to {out_path}")

