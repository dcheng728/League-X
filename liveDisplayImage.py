# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 18:10:42 2019

@author: dchen
"""
"""
from PIL import ImageGrab
from PIL import Image
"""
import cv2
import numpy as np
import time
import os
import tensorflow as tf
import time
from PIL import ImageGrab
from PIL import Image


#Load the tensorflow model and restore it
lol_model = tf.keras.models.load_model('my_model.h5')
lol_model.summary()
lol_model.load_weights("checkpoints/cp.ckpt")


#The path for all the images of the video we are analyzing
image_path = '20_2_2/'
file = open("selectedChampions.txt", "r")
selectedChampionsString = file.read()
class_names = selectedChampionsString.split(',')


KEEP_PLAYING = True

crop = 0

"""
This method takes a array of image list and outputs a prediction
"""
def predict(image_list):
    image_np = np.stack(image_list,axis = 0,)
    prediction = lol_model.predict(image_np)
    output = [np.argmax(prediction[n]) for n in range(prediction.shape[0])]
    return output, prediction

"""
@params: map image, background image
This method will use the red circle detection method to find all enemy champions
on a map, then it will find out what champions they are.
"""
def drawcircle(image,bg_image):
    global crop
    global croppath
    radius = 12 #the radius for all the circles to crop out
    
    cropped_list = [] #The list of all champions in an image
    
    b,g,r = cv2.split(image)
    inranger = cv2.inRange(r,120,255)
    inrangeg = cv2.inRange(g,120,255)
    inrangeb = cv2.inRange(b,120,255)
    
    induction = inranger - inrangeg - inrangeb
    
    circles = cv2.HoughCircles(induction,cv2.HOUGH_GRADIENT,1,10,param1 = 30,param2 =15,minRadius = 5, maxRadius = 30)
    
    #If there are champions detected
    if(circles is not None):
        for n in range(circles.shape[1]):
            x = int(circles[0][n][0])
            y = int(circles[0][n][1])
            try:
                crop_image = image[y-radius:y+radius,x-radius:x+radius].copy()
                cropped_list.append(crop_image)
                bg_image[10+n*30:10+n*30+24,300:324] = crop_image 
            except:
                pass
        cropped_imagees = np.array(cropped_list)
        champ_prediction, confidence = predict(cropped_imagees)
        
        for n in range(len(champ_prediction)):
            cv2.putText(bg_image,class_names[champ_prediction[n]],(330,30+n*30),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
            cv2.putText(bg_image,str(confidence[n][champ_prediction[n]]),(450,30+n*30),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
            
        for n in range(circles.shape[1]):
            
            x = int(circles[0][n][0])
            y = int(circles[0][n][1])
            
            cv2.rectangle(image,(x-radius,y-radius),(x+radius,y+radius),(255,255,255))
            

    bg_image[10:285,10:285] = img

    return bg_image


image_num = os.listdir(image_path) #Find number of images in the file
n = 0
img = cv2.imread(image_path+"0.jpg") 


#The main thread
while True:
    gui_background = np.zeros([400,600,3],dtype=np.uint8)
    #img = cv2.imread(image_path+str(n)+".jpg")
    image_pil = ImageGrab.grab((1645,805,1920,1080)).convert('RGB')
    opencv_image = np.array(image_pil)
    img = opencv_image[:,:,::-1].copy()
    img = drawcircle(img,gui_background)
    
    cv2.putText(img,str(n)+"/"+str(len(image_num)),(20,310),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    
    cv2.imshow("",img)
    k = cv2.waitKey(20)
        
    

    
    
    
    
    
    
    
    
    