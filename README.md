# DiceReader
Reese Ford, Dyla Deyhimi, Demetri Tyra\
Baylor University - ELC 4438 - Embedded Final Project

![An image of a device with a camera mounted above a dice mat with a d6 die on it](readme_images\cover_image.png)

## Project Summary
This device is a camera rig system that detects and audibly reads the number of a D6 dice roll on a D&D dice mat.

The device uses the Raspberry Pi Camera 3 Module to detect and capture a top-down image of a die on the mat. Using the image, the system uses a machine learning model with thousands of similar pictures to detect the number of the dice roll, from 1-6.  The device uses a small speaker to audibly read the rolled number.

The device is constructed using 2 PVC pipes joined with a PVC elbow connector. Attached to the top pipe is the Pi Camera, as well as a ring light that ended up not being utilized. All of this is attached to a piece of MDF that holds and aligns the dice mat and the Raspberry Pi itself.

### Project Objectives
1. **Camera Interface**: Properly take images with the Pi Camera 3, utilizing functions and image format.
2. **Machine Learning**: Creation of functioning ML model for identifying dice and reading number using large image datasets
3. **Accuracy**: Execution of model process through numerous epochs to improve accuracy
4. **Motion Detection**: The device uses OpenCV to store image information, when there is enough change in two consecutive images, motion is detected.
5. **Audio Output**: Using PyGame, the device will speak the dice roll out loud using text to speech or pre-recorded lines.

## Hardware
The Raspberry Pi 4 Model B was chosen as the hardware platform for its flexibility with an easy-to-use first party camera module, the RPi Camera Module 3.  The camera module connects to the RPi via ribbon cable into the Pi’s first party camera port.  Other hardware connections include USB connections from Pi to speaker and from battery bank to Pi.

### Hardware Design
![alt text](readme_images\schematic.png)

Peripherals include the Pi Camera 3 and an external battery bank to power the RPi and ring light.  Due to the design’s dependence on data transfer between the camera and the Pi, no GPIO connections were necessary.  The Raspberry Pi is compatible with the Pi Camera through a designated ribbon-cable header.

The system is powered by an INIU power bank using USB-A to USB-C connection to the Pi. This allows the device to be connected separately from an outlet power source for portability and usage of packages, models, and scripts saved on the SD card.

All connections are via USB and the parts are fixated onto a baseplate with the camera apparatus. Figure 2 shows the physical implementation of the Hardware.

1. Raspberry Pi 4 Model B (RPi)
2. Camera - Pi Camera Module 3
    * Compatible with libcamera-based python library, picamera2, to take and send pictures to Raspberry Pi and communicates with 2-wire serial (specifies that it supports I2C, but doesn’t list the default communication)
3. Ring Light
4. Speaker
    * Cheap USB speaker, compatible with PyGame library to output audio files called from python script
5.	Battery Bank – INIU model B1 – B41
    * Low power battery bank capable of safely powering Raspberry Pi

## Software
The general process for our software design was based around the method of creating and using a Machine Learning (ML) model to detect and read the number rolled on the dice. After this process was established, the state machine and logical flow were designed.

### Model Creation
In order to create a machine learning model, the most important thing to have is a dataset. So our first step was to create it, we did this by taking 10 images of each dice face at random spots on the dice mat. This gave us a dataset of 60 images, which is very tiny, and in order to do machine learning effectively, more than 500 images in a dataset is about the bare minimum if your model is very accurate. I did not want to take any risks and wanted to create a dataset that includes pretty much every scenario that could happen. In order to do this I decided I will create a dataset that has 5 degree rotations applied to every image from 0-366 degrees, this increased out dataset to about 4200 images. This was done with the file called: “rotate.py” in which it grabbed each image from the first dataset and injected each rotated image into a new directory. The next thing I wanted to do was to create more variations in the hue/brightness/exposure of the image, this was not something that I had any desire to code so I imputed the dataset into a software known as roboflow and within it, I was able to decide the degrees of change that each augmentation would do, meaning: 21 degrees of difference in brightness and exposure and 7 degrees of difference for hue. To make the dataset not be ridiculously big I used roboflow to randomly select about 2500 images from the 4200-image dataset and apply the hue/brightness/exposure augmentations, this increased the dataset size to 5050 images. Which I decided was a great amount for an extremely accurate model to be created.

Now after the dataset has been completely created, the next step is to create an object detection machine learning model. This would be way to difficult of a model to run on the small CPU of the RPi, so I had to use roboflow to create a model that can run on their own GPUs. To do this I had to open a photoshop style tool and individually draw a bounding box on each of the 5050 images. Once this painstaking process was completed, all I had to do was select the type of model, which was YOLOv8 . Now the process had to run over 300 epochs  while the model was getting its parameters’ weights changed until the maximum accuracy and speed was reached. 

We were able to call the model with an API key similar to how one would want to use an OpenAi API key. The model returned data which included the x and y image location of where it inferred the location of the dice to be in the image. We used this to create a file that crops each image that was imported to make it only show what is inside of a bounding box. Next, I used this to make a new folder of images that has every single image from the dataset, but this time was cropped to the size of the bounding box. 

Number recognition time, the script I created to do this trains a deep learning model to classify images into six categories (being the dice faces) using PyTorch (a library of python). It begins by resizing, normalizing, and converting the images into tensors . The dataset was then split into training and validation subsets that were based on specific naming patterns in the image filenames. The model I used was a pretrained ResNet18 model in which we fine tuned by replacing the final layer in it to match the output for the six output classes. Then I trained the model over 10 epochs using the Adam optimizer as well as a cross-entropy loss function, with the performance being tracked through some loss and accuracy metrics. Once it is done running the fully trained model is saved as a “.pth” file in order to be run later.

![alt text](readme_images\ml_1.png)

![alt text](readme_images\cropped_dice.png)

![alt text](readme_images\bounded_dice.png)

### State Machine
Because of the simplicity of the logic in our design (Scan, Speak, Repeat), a state machine is the best option for describing and programming the operation. In preliminary design, we tried to use an activity diagram, but looking at the state machine diagram shown below, it works much better as a state machine.

![alt text](readme_images\state_machine.png)

The flow of logic follows a very linear path: 
1. The program starts out in the WAITING_FOR_DICE state by taking two images, one slightly after another. By subtracting the images, the program can determine if there is motion between the two images.
    1. If there is motion detected, the program will loop back to the beginning of the step. Reading the top of the dice if there is still motion can leave the image blurry, or even read the dice too soon in some cases.
    2. If the images are similar enough (a standard deviation of less than 10), the program will then use our RoboFlow model (described in the Model Creation section) and the Inference library to determine if the second image (the most time-current image) contains a dice face. If the library is more than 75% confident that the image contains the “dice” class, the program will move to the DICE_DETECTED state.
    3. If the image doesn’t contain a dice face, the state will loop, trying again starting with motion detection. This allows us to roll the dice without the risk of “missing” it, as it will take at most one extra loop to detect the dice
2. In the DICE_DETECTED state, the program will then run our PyTorch model to read the number on the face. Although inference is a bit more complicated with PyTorch versus using RoboFlow’s library, it is still a relatively simple affair, inputting the image into the appropriate function, and getting effectively “Yes, and here is the number” as an output. 
    1. If the number is valid, the program will then concatenate a file path starter and the output number to create a file path to an audio file where the number is read. PyGame is then used to play that audio file. After the audio file finishes playing, the state is then set to WAITING_FOR_DICE_TO_LEAVE.
    2. If the number is not valid, the program will keep trying, but in our testing, the number model is very accurate, and if a dice face is detected (which is a prerequisite for this state, so thanks to causality, there is a face in the image), the number model will read a number. 
3.	Finally, in the WAITING_FOR_DICE_TO_LEAVE state, the program runs the same motion detection / face detection function, but instead of looking for the presence of the dice face, the state will only continue if there is no dice face detected.
    1. Like the WAITING_FOR_DICE, the state will loop until there is no motion detected and there is no face in the final image.
    2. Once the dice is removed, the program will move back to the WAITING_FOR_DICE state.

## Test Results
When we created the full number model for the first time, while testing it we saw no errors at all and every time it would read the right number perfectly. This lasted for about an hour, until we rolled a 3 in the corner of the dice mat and it outputted as a 5. After some trial and errors of seeing what was actually causing the errors we came to the conclusion that it just so happened that every instance of a 3 dice face being in the corner was in the validation set rather than the training set. Which means that the model was not trained at all in that very niche instance so it caused errors. This was an easy fix by re-training the number model and changing the training and validation sets to be actually random. 

There were also minor timing discrepancies, with the background programs and model inefficiencies causing the dice detection and audio output to take longer than expected on intervals. Regardless, the model training worked exceptionally well to the point of outlining the dice location consistently with 80%+ accuracy, as well as reading the number correctly with near 100% accuracy during testing and demonstration.  This is a direct result of the strenuous model work.

## Device Usage
1. Position device on a flat surface in a well lit location.
2. Plug in USB-c connector from battery bank to Raspberry Pi. This will start the Pi and run the dice reader script on boot. Wait for a chime from the speaker.
3. Roll the D6 die onto the dice mat. Wait for sound effects and spoken number.
4. Remove dice from the mat, out of the camera’s field of view. The program will return to looking for a dice object.
5. To power off, disconnect the Pi, and hope that it doesn’t corrupt the SD card.
