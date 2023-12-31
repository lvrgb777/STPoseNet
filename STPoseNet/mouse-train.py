from ultralytics import YOLO
import os
from tool.min_img_label import min_img


if __name__=='__main__':
    os.environ["WANDB_MODE"] = "offline"
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

    # first train use it to enhance data
    # min_img(r'F:\mouse_re\dataset\comprehensive-min')

    # Load a model
    model = YOLO('yolov8l-pose.yaml')  # build a new model from YAML
    model = YOLO('yolov8l-pose.pt')  # load a pretrained model (recommended for training)
    model = YOLO('yolov8l-pose.yaml').load('pretrain_weight.pt')  # build from YAML and transfer weights

    # Train the model
    model.train(data='mouse-pose.yaml', epochs=400, imgsz=640)
