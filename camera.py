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
from colorama import Fore, Back, Style
from datetime import datetime


model = load_model('model83.h5')

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')



cap = cv2.VideoCapture(0)


last_detected = datetime.now()

while True:
    ret, img = cap.read()
    # print("----")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # print(gray)
    # print("----")
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) #gets the parts of the image that contains a face

    # for(x,y,w,h) in faces:
    #     cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2) #draw a rectangle
    #     roi_gray = gray[y:y+h, x:x+w] #gets the region
    #     roi_color = img[y:y+h, x:x+w]
    #     smile = smile_cascade.detectMultiScale(roi_gray)
    #     for(ex,ey,ew,eh) in smile:
    #         cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2) #draw a rectangle
        roi_gray = gray[y:y + h, x:x + w]  # gets the region
        roi_color = img[y:y + h, x:x + w]
        mouth = smile_cascade.detectMultiScale(roi_gray)

        # boundaries for the actual mouth
        good_x = -1
        good_y = -1
        good_w = -1
        good_h = -1

        for (ex, ey, ew, eh) in mouth:
            if ey > good_y:  # the boundary containing the actual mouth will be as low as possible on the face
                good_x = ex
                good_y = ey
                good_w = ew
                good_h = eh

        if good_x == -1:
            continue

        mouth = roi_gray[good_y: good_y + good_h, good_x:good_x + good_w]

        mouth = cv2.resize(mouth, (52, 32))

        mouth = np.array(mouth)

        mouth = mouth.reshape((1, 32, 52, 1))
        mouth = mouth.astype("float32") / 255

        val = model.predict(mouth)
        val = val[0]

        y = np.where(val == np.amax(val))[0][0]

        txt = ''

        if y == 0:
            # print(Fore.RED + "cmon man grin some more")
            txt = 'no grin'
        else:
            # print(Fore.RED + "keep the grin going")
            txt = ' grin'

        cv2.rectangle(roi_color, (good_x, good_y), (good_x + good_w, good_y + good_h), (0, 255, 0), 2)

        cv2.putText(img, txt, (x, h), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
