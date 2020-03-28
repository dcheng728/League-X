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
import class_champions


#Load the tensorflow model and restore it
lol_model = tf.keras.models.load_model('my_model.h5')
lol_model.summary()
lol_model.load_weights("checkpoints/cp.ckpt")


#The path for all the images of the video we are analyzing
image_path = 'map_images/20_2_16/'
file = open("selectedChampions.txt", "r")
selectedChampionsString = file.read()
class_names = selectedChampionsString.split(',')

scannerMap = class_champions.leagueMap()
for championName in class_names:
    scannerMap.addChampion(class_champions.leagueChampion(championName))

scannerMap.champions[0].jungler = True



KEEP_PLAYING = True

crop = 0

def sigmoid(x):
    return 1/(1 + np.exp(-x))

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
    coord_list = [] #The list of all the coordinate of the champions
    
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
                coord_list.append((x,y))
                #bg_image[10+n*30:10+n*30+24,300:324] = crop_image 
            except:
                pass
            
        cropped_imagees = np.array(cropped_list)
        champ_prediction, confidence = predict(cropped_imagees)            
         
        for n in range(circles.shape[1]):
            x = int(circles[0][n][0])
            y = int(circles[0][n][1])
        #Update the scannerMap using the prediction
        for champion in scannerMap.champions:
            champion.image = np.zeros([24,24,3],dtype=np.uint8)
        try:
            for n in range(len(champ_prediction)):
                scannerMap.setChampionCoord(class_names[champ_prediction[n]],coord_list[n])
                scannerMap.setChampionImage(class_names[champ_prediction[n]],cropped_imagees[n])
                scannerMap.setChampionRecordTime(class_names[champ_prediction[n]],time.time())
        except:
            pass
    #Draw info from the scannerMap onto the image
    for n in range(len(class_names)):
        cv2.putText(bg_image,class_names[n],(330,30+n*30),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
        cv2.putText(bg_image,str(scannerMap.getChampionCoord(class_names[n])),(450,30+n*30),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
        bg_image[10+n*30:10+n*30+24,300:324] = scannerMap.champions[n].image
    #Draw the position of the jungler, the color of the jungler will become more transparent as time passes
    for champion in scannerMap.champions:
        if champion.coord and champion.jungler:
            time_past = time.time() - champion.time_recorded
                
            #It takes roughly 25 seconds to go from fully displayed to half transparent
            img[champion.coord[1]-12:champion.coord[1]+12,champion.coord[0]-12:champion.coord[0]+12] = cv2.addWeighted(img[champion.coord[1]-12:champion.coord[1]+12,champion.coord[0]-12:champion.coord[0]+12],0.3,
                            champion.minimap_image,0.7,0)
            
            

    bg_image[10:285,10:285] = img

    return bg_image


image_num = os.listdir(image_path) #Find number of images in the file
n = 99
img = cv2.imread(image_path+"99.jpg") 


#The main thread
while True:
    if n == len(image_num) - 1:
        break;    
    if KEEP_PLAYING:
        n = n + 1
    else:
        pass
    
    gui_background = np.zeros([335,600,3],dtype=np.uint8)
    img = cv2.imread(image_path+str(n)+".jpg")
    img = drawcircle(img,gui_background)
    #print(str(n) + "/" + str(len(image_num)))
    cv2.putText(img,str(n)+"/"+str(len(image_num)),(20,310),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    
    cv2.imshow("",img)
    k = cv2.waitKey(20)
    
    if (k == ord('q') or k == ord('Q')):
        KEEP_PLAYING = not KEEP_PLAYING
    elif (k == ord('a') or k == ord('A')):
        n = n - 1
    elif (k == ord('d') or k == ord('D')):
        n = n + 1
    elif (k == ord('r') or k == ord('R')):
        cv2.imwrite('gif_images/'+str(n)+'.jpg',img)
        
    

    
    
    
    
    
    
    
    
    