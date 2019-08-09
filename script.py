import numpy as np
import cv2 as cv
import json

face_cascade = cv.CascadeClassifier('/Users/skylergao/Downloads/HackSTL-2019-master-3/haarcascade_frontalface_default.xml')
mouth_cascade = cv.CascadeClassifier('/Users/skylergao/Downloads/HackSTL-2019-master-2/haarcascade_mcs_mouth.xml')
face = cv.imread("/Users/skylergao/Desktop/photo-1507003211169-0a1dd7228f2d.jpeg", 1)
gray = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in faces:
    cv.rectangle(face,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = face[y:y+h, x:x+w]
    mouth= mouth_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in mouth:
        cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

#cv.imshow('img',face)
#cv.waitKey(0)
#cv.destroyAllWindows()


isSmiling = False
data = {
    "isSmiling": isSmiling
}

with open("data.json", 'w') as f:
    json.dump(data, f)
