from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import time

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
picam2.set_controls({"ExposureTime": 10000})

encoder = H264Encoder(10000000)

picam2.start_recording(encoder, "camera-testing/video.h264")
time.sleep(5)
picam2.stop_recording()