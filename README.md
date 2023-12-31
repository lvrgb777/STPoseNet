# STPoseNet
This is a pose recognition model for laboratory mice based on yolov8

# The repository includes:
Source code of STposeNet built on YOLO v8
Training code for STposeNet
Data enhancement code for STposeNet
Keypoints identification program for STposeNet

# Using STposeNet:

## 1.Create a new environment
-conda create -n STPoseNet python=3.8

-pip install -r requirements.txt
## 2. run ./tool/min_img_label.py to perform data enhancement
## 3. run mouse-train.py to train weight for your experimental data
## 4. run mouse-pre to forecast result

# Other matters：
## Core module code location

The main modifications base on yolo v8  are located ./ultralytice/engine/predictor
