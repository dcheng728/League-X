import numpy as np
import cv2
import os
import random



script_crop_path = 'champs/' #Path that contains all headshots of the champs
save_path = 'training_set/'  #Path that the training sets and testing sets will be saved
test_ratio = 0.05 #Ratio of test images

champions_found = []

train_images = []
train_labels = []

test_images = []
test_labels = []

def create_class_txt():
    global champions_class
    """
    create a .txt file that records the index of class
    """
    file = open(save_path+'class.txt', 'w')
    for champion_name in os.listdir(script_crop_path):
        if champion_name in champions_class:
            file.write(str(champions_class.index(champion_name)) + 
                            ':' + 
                            str(champion_name)
                            + '\n')
    return True

def create_train_data():
    """
    Creates the .npy file of the training and testing sets
    """
    global toDisplay
    r_max = int(1/test_ratio)
    n = 1
    for champion_name in os.listdir(script_crop_path):
        if champion_name in champions_class:
            champions_found[champions_class.index(champion_name)] = 1
            for image in os.listdir(script_crop_path+champion_name+'/'):
                img = cv2.imread(script_crop_path+champion_name+'/'+image)
                img = cv2.resize(img,(24,24))
                r = random.randint(1,r_max)
                if r == 1:
                    test_images.append(img)
                    test_labels.append(champions_class.index(champion_name))
                else:
                    train_images.append(img)
                    train_labels.append(champions_class.index(champion_name))
            n = n + 1

def launchScanner():
    global train_images,train_labels,test_images,test_labels,champions_class,toDisplay,KEEP_DISPLAYING
    global champions_found
    
    KEEP_DISPLAYING = True
    train_images = []
    train_labels = []

    test_images = []
    test_labels = []
    
    #Open the file and read the selected champions from it
    file = open("selectedChampions.txt", "r")
    selectedChampionsString = file.readline()
    champions_class = selectedChampionsString.split(',')
    champions_found = [0 for n in range(len(champions_class))]
    
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
    print("Train labels size: " + str(train_labels.shape))
    print("Test images size : " + str(test_images.shape))
    print("Test labels size : " + str(test_labels.shape))
    champions_found_string = ''
    for n in range(len(champions_class)):
        if champions_found[n] == 0:
            champions_found_string = champions_found_string + str(champions_class[n]) + ": not found, "
        else:
            champions_found_string = champions_found_string + str(champions_class[n]) + ": found, " 
    print(champions_found_string)
    return champions_found






