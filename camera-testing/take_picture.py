from picamera2 import Picamera2
import time
from libcamera import controls

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.set_controls({"ExposureTime": 20000, "AfMode": controls.AfModeEnum.Continuous})
picam2.start()
picam2.capture_file("camera-testing/image.jpg")