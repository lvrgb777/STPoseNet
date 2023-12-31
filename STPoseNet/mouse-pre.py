from ultralytics import YOLO
import os


if __name__=='__main__':
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

    model = YOLO(model="The weight file trained in the second step (.\runs\pose\train\train\xxx.pt)")
    results = model(r"Video files that need to be identified")

    # # Call camera recognition
    # model = YOLO(model="trained_weight\\chase_min_l.pt")
    # results = model(0)


