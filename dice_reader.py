import cv2
import numpy as np
from enum import Enum
import pygame
import os

# Initilize PyGame
os.system("amixer sset Master 90%")
pygame.init()

class State(Enum):
    WAITING_FOR_DICE = 1
    DICE_DETECTED = 2
    SPEAK_NUMBER = 3
    WAITING_FOR_DICE_TO_LEAVE = 4

curr_state = State.WAITING_FOR_DICE

def dice_detected():
    face_detected = True
    # Motion Detection Loop
    # Look for Dice
    return face_detected

while True:
    if (curr_state == State.WAITING_FOR_DICE):
        dice_detect = dice_detected()

        # State Change
        if dice_detect == True:
            curr_state = State.DICE_DETECTED

    elif (curr_state == State.DICE_DETECTED):
        # Use Model to Detect Number
        dice_number = None

        # State Change
        if (dice_number != None):
            curr_state = State.SPEAK_NUMBER

    elif (curr_state == State.SPEAK_NUMBER):
        # Play Sound File based on dice_number
        my_sound = pygame.mixer.Sound('audio_files/dice_'+str(dice_number)+'.mp3')
        playing = my_sound.play()
        while playing.get_busy():
            pygame.time.delay(100)
        speaking = playing.get_busy()

        # State Change
        if (speaking == False):
            curr_state = State.WAITING_FOR_DICE_TO_LEAVE

    elif (curr_state == State.WAITING_FOR_DICE_TO_LEAVE):
        dice_detect = dice_detected()
        dice_detect = False

        # State Change
        if dice_detect == False:
            curr_state = State.WAITING_FOR_DICE

    else:
        curr_state = State.WAITING_FOR_DICE