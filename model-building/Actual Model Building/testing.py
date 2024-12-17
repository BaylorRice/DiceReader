from inference import get_model
import supervision as sv
import cv2
import os
"""
This creates a jpg image that has the original raw image that is run 
through the roboflow model with the bounding box annotated over it
"""
os.environ["ROBOFLOW_API_KEY"] = "J9tV3kwjI7eWiwKtmw4h"
image = "d6_pics/augmented/1_1_0.jpg"
model = get_model(model_id="dice-finder-qey6z/1")
results = model.infer(image)[0]
print(results)
detections = sv.Detections.from_inference(results)
bounding_box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()
annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)
annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
cv2.imwrite("camera-testing/detected.jpg", annotated_image)