from keras import layers
from keras import models
from keras.datasets import mnist
from keras.datasets import cifar10
from keras.utils import to_categorical
from numpy import loadtxt
from keras.models import load_model
import cv2
import numpy as np
import pandas as pd
import random
from keras.models import Model

#creates the model for classifying

# model = load_model('model.h5')
# # summarize model.
# model.summary()

#get the data

#training size: 13026
#testing size: 3260

all_images = [] #x
all_labels = [] #y

#gets the mouths
for i in range(16286):
    img = cv2.imread("bettermouths/mouth" + str(i + 1) + ".png", -1)
    all_images.append(img)

#gets the labels
with open('labels/usedlabels.txt') as f:
    content = f.readlines()
all_labels = [x.strip() for x in content]


for i in range(len(all_labels)): #formats the labels into int
    num = int(all_labels[i])
    if num == -1:
        num = 0
    all_labels[i] = num


train_images = []
test_images = []
train_labels = []
test_labels = []

#adds randomly to the train and test dataset
for i in range(13026):
    index = random.randint(0, len(all_images) - 1)
    train_images.append(all_images.pop(index))
    train_labels.append([all_labels.pop(index)])


for i in range(3260):
    index = random.randint(0, len(all_images) - 1)
    test_images.append(all_images.pop(index))
    test_labels.append([all_labels.pop(index)])


train_images = np.array(train_images)
test_images = np.array(test_images)
train_labels = np.array(train_labels)
test_labels = np.array(test_labels)

#formats the images and labels
train_images = train_images.reshape((13026 , 32, 52, 1))
train_images = train_images.astype("float32") / 255
test_images = test_images.reshape((3260, 32, 52, 1))
test_images = test_images.astype("float32") / 255

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)


#create the model

model = models.Sequential()
model.add(layers.Conv2D(20,(3,3),activation="relu", input_shape=(32,52,1)))
model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Dropout(0.2))
model.add(layers.Conv2D(50, (3, 3), activation="relu"))
model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Dropout(0.2))
# model.add(layers.Conv2D(64, (3, 3), activation="relu"))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Dropout(0.2))
# model.add(layers.Conv2D(128, (3, 3), activation="relu"))
model.add(layers.Flatten())
model.add(layers.Dense(2, activation="softmax"))

#
# def model(in_shape=(32,52,1), n_classes=2, opt='sgd'):
#     in_layer = layers.Input(in_shape)
#     conv1 = layers.Conv2D(filters=20, kernel_size=5,
#                           padding='same', activation='relu')(in_layer)
#     pool1 = layers.MaxPool2D()(conv1)
#     conv2 = layers.Conv2D(filters=50, kernel_size=5,
#                           padding='same', activation='relu')(pool1)
#     pool2 = layers.MaxPool2D()(conv2)
#     flatten = layers.Flatten()(pool2)
#     dense1 = layers.Dense(10, activation='relu')(flatten)
#     preds = layers.Dense(n_classes, activation='softmax')(dense1)
#
#     model = Model(in_layer, preds)
#     model.compile(loss="categorical_crossentropy", optimizer=opt,
# 	              metrics=["accuracy"])
#     return model


#format - conv20, maxpooling2d, conv50, maxpooling, flatten, dense


# model = model()

model.compile(loss="categorical_crossentropy",optimizer="sgd", metrics=["accuracy"]) #settings for the model
model.fit(train_images, train_labels, batch_size=150, epochs=10, verbose=1) #train the model
test_loss, test_acc = model.evaluate(test_images, test_labels) #evaluate on the test set
print("Test accuracy:", test_acc)



model.save("model.h5")
print("saved model")
