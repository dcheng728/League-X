# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 22:33:00 2019
This file trains the CNN that takes care of the champion recognition
@author: dchen
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf
import numpy as np
#from tensorflow.keras import datasets, layers, models
from tensorflow import keras
import cv2
import os
import time

file = open("selectedChampions.txt", "r")
selectedChampionsString = file.read()
class_names = selectedChampionsString.split(',')


#Define a checkpoint path and a checkpoint saving callback
checkpoint_path = "checkpoints/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)


#Load the training sets and testing sets created earlier
train_images = np.load("training_set/train_images.npy")
train_labels = np.load("training_set/train_labels.npy")
test_images = np.load("training_set/test_images.npy")
test_labels = np.load("training_set/test_labels.npy")


#Make sure that the training set and testing set are not empty
assert not np.any(np.isnan(train_images))
assert not np.any(np.isnan(test_images))

# Normalize pixel values to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0


#Define the model
model = keras.models.Sequential()
model.add(keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(24, 24,3)))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid'))
model.add(keras.layers.Conv2D(32, (3, 3), activation='relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid'))

model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(12,kernel_regularizer=keras.regularizers.l2(0.001), activation='relu'))
model.add(keras.layers.Dense(5, activation='softmax'))

#Print a summary of the model
model.summary()


#Compile the model
model.compile(optimizer= "Adadelta",
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])



history = model.fit(train_images, train_labels, epochs=100, callbacks=[cp_callback])

test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test Accuracy：' + str(test_acc*100) + '%')
#model.save('model/my_model.h5')
model.save('my_model.h5')

"""
def predict(image_list):
    image_np = np.stack(image_list,axis = 0,)
    prediction = lol_model.predict(image_np)
    output = [np.argmax(prediction[n]) for n in range(prediction.shape(0))]
    return output

vis_images = np.load("visualize_set/visualize_images.npy")
prediction = model.predict(vis_images)
model.save('my_model.h5')
for n in range(prediction.shape[0]):
    print(np.argmax(prediction[n]))
"""