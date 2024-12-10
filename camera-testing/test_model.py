from inference import get_model
import supervision as sv
import cv2
from picamera2 import Picamera2
import time
from libcamera import controls
import os

os.environ["ROBOFLOW_API_KEY"] = "J9tV3kwjI7eWiwKtmw4h"

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.set_controls({"ExposureTime": 10000, "AfMode": controls.AfModeEnum.Manual, "LensPosition": 2.0})
picam2.start()
image = picam2.capture_array()
cropped = image[0:2592, 350:3600]

model = get_model(model_id="dice-finder-qey6z/1")

results = model.infer(cropped)[0]
print("")
print(results)
print("")

# load the results into the supervision Detections api
detections = sv.Detections.from_inference(results)

# create supervision annotators
bounding_box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# annotate the image with our inference results
annotated_image = bounding_box_annotator.annotate(
    scene=cropped, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)

# display the image
cv2.imwrite("camera-testing/detected.jpg", annotated_image)