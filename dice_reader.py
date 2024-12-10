import cv2
import numpy as np
from enum import Enum

class State(Enum):
    WAITING_FOR_DICE = 1
    DICE_DETECTED = 2
    SPEAK_NUMBER = 3
    WAITING_FOR_DICE_TO_LEAVE = 4

curr_state = State.WAITING_FOR_DICE

def dice_detected():
    face_detected = False
    # Motion Detection Loop
    # Look for Dice
    return face_detected

while True:
    if (curr_state == State.WAITING_FOR_DICE):
        dice_detect = dice_detected()
        dice_detect = False
        if dice_detect == True:
            curr_state = State.DICE_DETECTED

    elif (curr_state == State.DICE_DETECTED):
        # Use Model to Detect Number
        dice_number = None
        if (dice_number != None):
            curr_state = State.SPEAK_NUMBER

    elif (curr_state == State.SPEAK_NUMBER):
        # Pygame to speak number file
        speak_done = False
        if (speak_done == True):
            curr_state = State.WAITING_FOR_DICE_TO_LEAVE

    elif (curr_state == State.WAITING_FOR_DICE_TO_LEAVE):
        dice_detect = dice_detected()
        dice_detect = True
        if dice_detect == False:
            curr_state = State.WAITING_FOR_DICE

    else:
        curr_state = State.WAITING_FOR_DICE