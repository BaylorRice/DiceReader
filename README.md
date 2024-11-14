# DiceReader
Python Dice Reader

## Statement of Work
We will create a dice roll detector, this will be done with a d6 die rolled in a dice mat, with a camera likely mounted on the dice mat. This camera will read the dnd style die and the rpi will speak the dice roll outloud with a speaker. We would like to make this whole setup as small as possible in relation to the dice mat, including a small battery pack for it to run. When the camera detects when the die has stopped moving it will take a picture, then transforming the image into a format that the machine learning library can read accurately. Once it has been read, it will be spoken by this speaker that will likely use a text to speech library. 
Reach goals: reading other types of dice such as a d20, and using our own voices as the dice roll speakers, ie: it saying: "You rolled a 6! Not Bad." Another goal would be to have it read a few die at the same time and add their values together. Another goal would be to have Dr. Potter voice act for it.  Have settings for if the multiple dice are multiplied or read individually, ect. This could be controlled from a website or buttons. 
