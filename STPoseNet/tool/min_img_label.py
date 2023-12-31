import copy
import os
import numpy as np
import cv2 as cv
import random


def ObtainRandom(n):
    list_info = []  # 定义一个空列表（用于接收产生的随机数）
    list_ = int(n/10)
    while list_ != 0:
        info = random.randint(1, n)  # 每次循环获取一次随机数
        if info not in list_info:  # 判断随机数是否在列表中
            list_info.append(info)  # 不在列表中 进行添加
            list_ = list_-1
    return list_info

def min_img(path):
    labels_path = path + '\\labels\\'
    imgs_path = path + '\\images\\'
    items = ('train', 'val')

    total_num = len(os.listdir(imgs_path + 'train')) + len(os.listdir(imgs_path + 'val'))
    val_list = ObtainRandom(total_num)

    for k, item in enumerate(items):
        if item == 'train':
            m = total_num - len(val_list)
        if item == 'val':
            m = len(val_list)
        list_txt = os.listdir(labels_path + item + '\\')
        for j, file in enumerate(list_txt):
            if j < m:
                file_name = file.split('.')
                if file_name[0] not in items:
                    img_path = imgs_path + item + '\\' + file_name[0] + '.jpg'
                    img = cv.imread(img_path)
                    # print(img_path)
                    img_size = img.shape
                    file_path = os.path.join(labels_path + item + '\\', file)
                    with open(file_path, "r") as labels:
                        label = labels.readlines()
                        label = label[0].split(" ")[1:-1]
                        for i in range(8):
                            label.remove('')
                        for i in range(3):
                            label.remove('2.000000')
                        label = list(map(float, label))

                        label_ = np.zeros(10)
                        for i in range(10):
                            if i % 2 == 0:
                                label_[i] = label[i] * img_size[1]
                            if i % 2 == 1:
                                label_[i] = label[i] * img_size[0]
                        label_int = label_.astype(int)

                        min_box = [[label_int[0]-label_int[2], label_int[1]-label_int[3]], [label_int[0]+label_int[2], label_int[1]+label_int[3]]]
                        for i in range(2):
                            if min_box[i][0] > img_size[1]:
                                min_box[i][0] = img_size[1]
                            if min_box[i][0] < 0:
                                min_box[i][0] = 0
                        for i in range(2):
                            if min_box[i][1] > img_size[0]:
                                min_box[i][1] = img_size[0]
                            if min_box[i][1] < 0:
                                min_box[i][1] = 0
                        min_img = img[min_box[0][1]:min_box[1][1], min_box[0][0]:min_box[1][0], :]

                        # print(j)
                        # print(label_int[0:4])
                        # print(min_box)
                        # cv.imshow('img', min_img)
                        # cv.waitKey()

                        min_img_size = min_img.shape
                        tf_set = min_box[0]
                        img_kps = copy.deepcopy(label_[4:])
                        min_kps = np.zeros(6)
                        for i in range(3):
                            min_kps[i * 2] = img_kps[i * 2] - tf_set[0]
                            min_kps[i * 2 + 1] = img_kps[i * 2 + 1] - tf_set[1]

                        i = len(list_txt) + total_num
                        min_name = 'min_' + file_name[0]

                        min_img_path = imgs_path + item + '\\' + min_name + '.jpg'
                        min_label_path = labels_path + item + '\\'
                        cv.imwrite(min_img_path, min_img)

                        f_txt = open(os.path.join(min_label_path + min_name + '.txt'), 'w')
                        f_txt.write("%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" %
                                    (0, 0.5, 0.5, 0.5, 0.5,
                                     min_kps[0] / min_img_size[1], '', min_kps[1] / min_img_size[0], '', str(2.000000), '',
                                     min_kps[2] / min_img_size[1], '', min_kps[3] / min_img_size[0], '', str(2.000000), '',
                                     min_kps[4] / min_img_size[1], '', min_kps[5] / min_img_size[0], '', str(2.000000)
                                     ))
                        f_txt.close()
