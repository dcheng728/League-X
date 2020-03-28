import numpy as np
import cv2
import os
import random


script_crop_path = 'champs/'
save_path = 'training_set/'
champion_class = []
test_ratio = 0.05

train_images = []
train_labels = []

test_images = []
test_labels = []


def create_class_txt():
    """
    create a .txt file that records the index of class
    """
    file = open(save_path+'class.txt', 'w')
    for champion_name in os.listdir(script_crop_path):
        champion_class.append(champion_name)
        file.write(str(champion_class.index(champion_name)) + 
                        ':' + 
                        str(champion_name)
                        + '\n') 
    return True

def create_train_data():
    r_max = int(1/test_ratio)
    for champion_name in os.listdir(script_crop_path):
        for image in os.listdir(script_crop_path+champion_name+'/'):
            img = cv2.imread(script_crop_path+champion_name+'/'+image)
            img = cv2.resize(img,(24,24))
            r = random.randint(1,r_max)
            if r == 1:
                test_images.append(img)
                test_labels.append(champion_class.index(champion_name))
            else:
                train_images.append(img)
                train_labels.append(champion_class.index(champion_name))
    
create_class_txt()
create_train_data()

train_images = np.array(train_images)
train_labels = np.array(train_labels)
test_images = np.array(test_images)
test_labels = np.array(test_labels)

np.save(save_path +"train_images", train_images)
np.save(save_path +"train_labels", train_labels)
np.save(save_path +"test_images", test_images)
np.save(save_path +"test_labels", test_labels)
print("--------------------------------------------")
print("Train images size: " + str(train_images.shape))
print("Train labels size: " + train_labels.shape)
print("Test images size : " + test_images.shape)
print("Test labels size : " + test_labels.shape)

