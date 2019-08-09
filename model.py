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


# model = load_model('model.h5')
# # summarize model.
# model.summary()

#get the data

#training size: 13026
#testing size: 3260

all_images = []
all_labels = []

for i in range(16286):
    img = cv2.imread("bettermouths/mouth" + str(i + 1) + ".png", -1)
    all_images.append(img)


with open('labels/usedlabels.txt') as f:
    content = f.readlines()
all_labels = [x.strip() for x in content]


for i in range(len(all_labels)):
    num = int(all_labels[i])
    if num == -1:
        num = 0
    all_labels[i] = num


train_images = []
test_images = []
train_labels = []
test_labels = []


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


train_images = train_images.reshape((13026 , 32, 52, 1))
train_images = train_images.astype("float32") / 255
test_images = test_images.reshape((3260, 32, 52, 1))
test_images = test_images.astype("float32") / 255

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)


model = models.Sequential()
model.add(layers.Conv2D(16,(3,3),activation="relu", input_shape=(32,52,1)))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Dropout(0.2))
model.add(layers.Conv2D(32, (3, 3), activation="relu"))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Dropout(0.2))
model.add(layers.Conv2D(64, (3, 3), activation="relu"))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Dropout(0.2))
model.add(layers.Flatten())
model.add(layers.Dense(2, activation="softmax"))


model.compile(loss="categorical_crossentropy",optimizer="sgd", metrics=["accuracy"])
model.fit(train_images, train_labels, batch_size=75, epochs=10, verbose=1)
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("Test accuracy:", test_acc)


#
#
# # num = 23
# #
# # print(test_images[num])
# #
# # cv2.imshow('image', test_images[num])
# # cv2.waitKey(0)
# #
# #
# # label = model.predict(test_images)
# #
# # print(np.where(label[num] == np.amax(label[num])))
# #
# # print(test_labels[num])
#
# #
model.save("model.h5")
print("saved model")
