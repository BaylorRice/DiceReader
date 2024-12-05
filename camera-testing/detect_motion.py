import cv2
import numpy as np
from picamera2 import Picamera2
import time
from libcamera import controls
import sys

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.set_controls({"ExposureTime": 10000, "AfMode": controls.AfModeEnum.Manual, "LensPosition": 2.0})
picam2.start()

image = picam2.capture_array()
current = image[0:2592, 350:3600]
time.sleep(0.5)

try:
    while True:
        previous = current
        time.sleep(0.1)

        image = picam2.capture_array()
        current = image[0:2592, 350:3600]

        image1 = current
        image2 = previous
        height, width, channels = current.shape

        diff = cv2.absdiff(image1, image2)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        mean, stdev = cv2.meanStdDev(mask)
        print("Mean:",mean,"Std:",stdev)

        if (stdev > 10):
            print("Motion Detected")
        else:
            print("No Motion Detected")

except KeyboardInterrupt:
    print("Detected Keyboard Interrupt")
    sys.exit()