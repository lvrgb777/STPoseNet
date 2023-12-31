# STPoseNet
This is a pose recognition model for laboratory mice based on yolov8.

## The repository includes:

Source code of STposeNet built on YOLO v8
Training code for STposeNet
Data enhancement code for STposeNet
Keypoints identification program for STposeNet

## Using STPoseNet

### **Create a new environment**  

[requirements.txt](https://github.com/lvrgb777/STPoseNet/blob/master/STPoseNet/requirements.txt) supports the normal running of STPoseNet. Before using STPoseNet, ensure that the environment is configured according to this file.  
```
-conda create -n STPoseNet python=3.8
-pip install -r requirements.txt
```
### **Dataset preparation** 

In this folder [datasets](https://huggingface.co/lvrgb777/STPoseNet/tree/main/dataset), We provide train dataset and test images and video.  

### **Pretrain weight preparation** 

This file [weight](https://huggingface.co/lvrgb777/STPoseNet/blob/main/yolov8l_pose_mouse_com.pt) ,We provide pretrain weight

### **training or testing** 

After abtaining the dataset and model, running [test.py](https://github.com/XZH-James/NeuroSeg2/blob/main/NeuroSeg%E2%85%A1-main/NeuroSeg%E2%85%A1-main/test.py) to test the image.  
Running [train.py](https://github.com/XZH-James/NeuroSeg2/blob/main/NeuroSeg%E2%85%A1-main/NeuroSeg%E2%85%A1-main/train.py) to train the new dataset.

### **The result** 
2. run ./tool/min_img_label.py to perform data enhancement
3. run mouse-train.py to train weight for your experimental data
4. run mouse-pre to forecast result

## Other matters
## Core module code location
The main modifications base on yolo v8  are located ./ultralytice/engine/predictor

## Contact information

If you have any questions about this project, please feel free to contact us. Email address: 13781672351@163.com
