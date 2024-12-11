import cv2
from enum import Enum
import pygame
import os
import sys
import time
from picamera2 import Picamera2
from libcamera import controls
from inference import get_model
import supervision as sv

try:
    # Initilize PyGame
    os.system("amixer sset Master 50%")
    pygame.init()
    
    # Initilize Roboflow Inference
    from dotenv import load_dotenv
    load_dotenv()
    ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
    model = get_model(model_id="dice-finder-qey6z/1")

    # Initialize Camera
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration()
    picam2.configure(camera_config)
    picam2.set_controls({"ExposureTime": 10000, "AfMode": controls.AfModeEnum.Manual, "LensPosition": 2.0})
    picam2.start()

    # State Machine Enumeration
    class State(Enum):
        WAITING_FOR_DICE = 1
        DICE_DETECTED = 2
        SPEAK_NUMBER = 3
        WAITING_FOR_DICE_TO_LEAVE = 4

    curr_state = State.WAITING_FOR_DICE_TO_LEAVE

    # Define Functions
    def dice_detected():
        global cropped_face_image
        global curr_state

        face_detected = False

        ## Motion Detection Loop
        # Take t(0) image
        image = picam2.capture_array()
        current = image[0:2592, 350:3600]
        motion_detected = True

        while motion_detected:
            # Set t(0) Image
            previous = current
            time.sleep(0.1)

            # Take t(1) Image
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
                motion_detected = True
            else:
                print("No Motion Detected")
                motion_detected = False
                face_image = image1

        ## Look for Dice
        results = model.infer(face_image)[0]

        if len(results.predictions) > 0:
            pred = results.predictions[0]
            if pred.class_name == "dice":
                if (pred.confidence >= 0.75):
                    face_detected = True

        if face_detected and curr_state == State.WAITING_FOR_DICE:
            right_face_image =cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)

            x_center = pred.x
            y_center = pred.y
            width = pred.width
            height = pred.height

            x_min = int(x_center - width/2)
            x_max = int(x_center + width/2)
            y_min = int(y_center - height/2)
            y_max = int(y_center + height/2)

            cropped_face_image = right_face_image[y_min:y_max, x_min:x_max]

        return face_detected

    def play_audio(filename):
        my_sound = pygame.mixer.Sound(filename)
        playing = my_sound.play()
        while playing.get_busy():
            pygame.time.delay(100)
        speaking = playing.get_busy()
        return speaking

    # Start Confirm Audio
    play_audio('audio_files/finished_startup.wav')

    # Main Loop
    while True:
        if (curr_state == State.WAITING_FOR_DICE):
            dice_detect = dice_detected()

            # State Change
            if dice_detect == True:
                curr_state = State.DICE_DETECTED

        elif (curr_state == State.DICE_DETECTED):
            cv2.imwrite("cropped.jpg", cropped_face_image)
            # Use Model to Detect Number
            print("Dice Detected!")
            dice_number = None

            # State Change
            if (dice_number != None):
                curr_state = State.SPEAK_NUMBER

        elif (curr_state == State.SPEAK_NUMBER):
            # Play Sound File based on dice_number
            speaking = play_audio('audio_files/dice_'+str(dice_number)+'.mp3')

            # State Change
            if (speaking == False):
                curr_state = State.WAITING_FOR_DICE_TO_LEAVE

        elif (curr_state == State.WAITING_FOR_DICE_TO_LEAVE):
            dice_detect = dice_detected()

            # State Change
            if dice_detect == False:
                curr_state = State.WAITING_FOR_DICE

        else:
            curr_state = State.WAITING_FOR_DICE


except KeyboardInterrupt:
    print("Detected Keyboard Interrupt")
    sys.exit()