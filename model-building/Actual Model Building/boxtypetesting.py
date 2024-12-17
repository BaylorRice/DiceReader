import cv2
from inference import get_model
import supervision as sv
import os

"""
This uses the api of the roboflow model and sends an image through the model and then shows a 
figure of the full image with the bounded box around it and an image cropped to the dimensions of the box, 
this was used in order to determine the scaling necessary to crop everything outside of the bounding box

"""

os.environ["ROBOFLOW_API_KEY"] = "J9tV3kwjI7eWiwKtmw4h"

image_path = "d6_pics_2/augmented/6_3_15.jpg"


model = get_model(model_id="dice-finder-qey6z/1")

results = model.infer(image_path)[0]

if results.predictions:
    pred = results.predictions[0]
    x = pred.x
    y = pred.y
    width = pred.width
    height = pred.height


    print(x, y, width, height)

x_min = int(x - width/2)
x_max = int(x + width/2)
y_min = int(y - height/2)
y_max = int(y + height/2)

print("Inference results:", results)
detections = sv.Detections.from_inference(results)

bounding_box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

image = cv2.imread(image_path)
cropped = image[y_min:y_max, x_min:x_max]
cv2.imshow("Cropped Image", cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
