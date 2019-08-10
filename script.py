import numpy as np
import cv2 as cv
import json
from keras import layers
from keras import models
from keras.datasets import mnist
from numpy import loadtxt


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



#load everything
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
mouth_cascade = cv.CascadeClassifier('haarcascade_mcs_mouth.xml')

model = load_model('model83.h5')

def getExtension():
    with open('info.json') as json_file:
        data = json.load(json_file)
        return data["data"]["extension"]


print("got extension")

extension = getExtension()

# if extension == "jpg": #so the file is found
#     extension = "jpeg"


face = cv.imread("media." + extension, -1)
gray = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

mouth = -1

print("finding face")

for(x,y,w,h) in faces:
    roi_gray = gray[y:y+h, x:x+w] #gets the region
    roi_color = face[y:y+h, x:x+w]
    mouth = mouth_cascade.detectMultiScale(roi_gray)


    #boundaries for the actual mouth
    good_x = -1
    good_y = -1
    good_w = -1
    good_h = -1


    for(ex,ey,ew,eh) in mouth:
        if ey > good_y: #the boundary containing the actual mouth will be as low as possible on the face
           good_x = ex
           good_y = ey
           good_w = ew
           good_h = eh

    if good_x == -1:
        continue

    mouth = roi_gray[good_y: good_y + good_h, good_x:good_x + good_w] #got the mouth

#now we see if the mouth is smiling

print("finding")

mouth = cv2.resize(mouth, (52, 32))

mouth = np.array(mouth)

mouth = mouth.reshape((1, 32, 52, 1))
mouth = mouth.astype("float32") / 255

val = model.predict(mouth)
val = val[0]

value = np.where(val == np.amax(val))[0]

print(value[0])

isSmiling = str(value[0])
data = {
    "isSmiling": isSmiling
}

with open("smiling.json", 'w') as f:
    json.dump(data, f)

print("dumped")
