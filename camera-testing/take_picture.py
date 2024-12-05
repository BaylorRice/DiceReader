from picamera2 import Picamera2
import time
from libcamera import controls
import cv2

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.set_controls({"ExposureTime": 10000, "AfMode": controls.AfModeEnum.Manual, "LensPosition": 2.0})
picam2.start()
picam2.capture_file("camera-testing/image.jpg")
image = cv2.imread("camera-testing/image.jpg")
cropped = image[0:2592, 463:4000]
cv2.imwrite("camera-testing/cropped.jpg", cropped)