import os, cv2


print("yes")

#load the cascades

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')


#get all the labels of the pictures


filename = 'labels/alllabels.txt'

with open(filename) as f:
    content = f.readlines()
alllabels = [x.strip() for x in content]

#now process the images

directory_in_str = "C:/Users/ashay/Desktop/HACKSTL/images"

directory = os.fsencode(directory_in_str)

num = 0

counter = 0


goodlabels = []

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     counter += 1
     # print(counter)
     # if counter == 1000:
     #     break
     # print(filename)
     if filename.endswith(".jpg") or filename.endswith(".JPEG"):
         # print(os.path.join(directory, filename))
         img = cv2.imread('images/' + filename,1)
         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
         faces = face_cascade.detectMultiScale(gray, 1.3, 5) #gets the parts of the image that contains a face
         for(x,y,w,h) in faces:
             # cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2) #draw a rectangle
             roi_gray = gray[y:y+h, x:x+w] #gets the region
             roi_color = img[y:y+h, x:x+w]
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

             num += 1

             mouth = roi_gray[good_y: good_y + good_h, good_x:good_x + good_w] #the mouth


             print(counter)

             cv2.imwrite('mouths/mouth' + str(num) + ".png", mouth) #download the mouth

             lab = alllabels[counter-1]

             goodlabels.append(lab) #add the label of the mouth



# print(len(goodlabels))

with open("labels/usedlabels.txt", "w") as f: #save the labels of the mouth to a text file
    for line in goodlabels:
        f.write(line)
        f.write("\n")
        # print("wrote")



# print(num)

# img = cv2.imread('images/0a7c576672f111e29f1422000a1fbc0e_6.jpg',1)
#
# # img = cv2.imread('lebron james face.png',1)
#
#
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# # cv2.imshow('img', gray)
# #
# # cv2.waitKey(0)
#
# faces = face_cascade.detectMultiScale(gray, 1.3, 5) #gets the parts of the image that contains a face
#
# for(x,y,w,h) in faces:
#     print("found face")
#     cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2) #draw a rectangle
#     roi_gray = gray[y:y+h, x:x+w] #gets the region
#     roi_color = img[y:y+h, x:x+w]
#     mouth = mouth_cascade.detectMultiScale(roi_gray)
#     for(ex,ey,ew,eh) in mouth:
#         cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)
#
#
# cv2.imshow('img', img)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
