import cv2, os


#now, we will make all the mouths the same size


directory_in_str = "C:/Users/ashay/Desktop/HACKSTL/mouths"
directory = os.fsencode(directory_in_str)

# smallest_width = 1000000
# smallest_height = 1000000
#
# total_width = 0
# total_height = 0

number = 0

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".png") or filename.endswith(".PNG"):
         # print(filename)
         img = cv2.imread("mouths/" + filename, -1)

         img = cv2.resize(img, (52, 32)) #resize

         number += 1

         cv2.imwrite("bettermouths/" + filename, img)

         print(number)
         #
         # total_width += shape[0]
         # total_height += shape[1]
         #
         # if smallest_width > shape[0]:
         #     smallest_width = shape[0]
         #
         # if smallest_height > shape[1]:
         #     smallest_height = shape[1]
         #
         # number += 1


print("done")

# avg_width = total_width / number
# avg_height = total_height / number
#
#
# print(avg_width)
# print(avg_height)
