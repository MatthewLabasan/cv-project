import cv2 # open cv module
import pytesseract # ocr module
from PIL import Image # pillow: image processing
import numpy as np

# don't need line below as long as you set up a virtual env and reinstall requirements and tesseract. not sure how to do tesseract on windows yet!
# use path to tesseract executable. to find this on mac: `which tesseract`. to find this on windows: `where tesseract``
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# load the frame
img1 = cv2.imread('./test_images/sandIslandTest1_live.png')
img2 = cv2.imread('./test_images/GUI.png')
img3 = cv2.imread('./test_images/sandIslandTest2.png')

# processing recommendations
# img1 = cv2.resize(img1, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC) # rescale
# img2 = cv2.resize(img2, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC) # rescale
# img3 = cv2.resize(img3, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC) # rescale
# img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) # grayscale
# img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) # grayscale
# img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY) # grayscale
# kernel = np.ones((2, 2), np.uint8) # erodes to be white only if all pixels within array size
# cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1] # thershold to binary
# img1 = cv2.dilate(img1, kernel, iterations=1) # remove noise (done on binary images?)
# img1 = cv2.erode(img1, kernel, iterations=1)
# cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1] # thershold to binary
# img2 = cv2.dilate(img2, kernel, iterations=1) # remove noise (done on binary images?)
# img2 = cv2.erode(img2, kernel, iterations=1)
# cv2.threshold(img3, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1] # thershold to binary
# img3 = cv2.dilate(img3, kernel, iterations=1) # remove noise (done on binary images?)
# img3 = cv2.erode(img3, kernel, iterations=1)

# so far, image 1 (normal scale, direct screenshot) runs best without any processing at all. 
# probably safe to say that normal frame of full resolution will be fine
# detection of dials, yet difficulty in reading, correct results often in []

# get size 
h1Img, w1Img = img1.shape[0], img1.shape[1] # returns third value we don't need, unless grayscale
h2Img, w2Img = img2.shape[0], img2.shape[1]
h3Img, w3Img = img3.shape[0], img3.shape[1]

# detect text on img
print("img1: \n" + pytesseract.image_to_string(img1) + "\n") 
print("img2: \n" + pytesseract.image_to_string(img2) + "\n")
print("img3: \n" + pytesseract.image_to_string(img3) + "\n")

# show bounding box
box1 = pytesseract.image_to_boxes(img1) # gives string with coordinate values & width/height for chars
box2 = pytesseract.image_to_boxes(img2)
box3 = pytesseract.image_to_boxes(img3)

data1 = pytesseract.image_to_data(img2)
print(data1)
print("--------")
print(data1.splitlines())
print("--------")
print(enumerate(data1.splitlines()))
data2 = pytesseract.image_to_data(img2)
data3 = pytesseract.image_to_data(img3)

# character boxes
# for a in box1.splitlines(): # converts string of values into a list of values
#     a = a.split()
#     x, y = int(a[1]), int(a[2])
#     width, height = int(a[3]), int(a[4])

#     cv2.rectangle(img1, (x, h1Img - y), (width, h1Img - height), (255, 0, 0), 1) # xy base, wh. color, thickness
#     cv2.putText(img1, a[0], (x, h1Img - y + 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

# for a in box2.splitlines(): # converts string of values into a list of values
#     a = a.split()
#     x, y = int(a[1]), int(a[2])
#     width, height = int(a[3]), int(a[4])

#     cv2.rectangle(img2, (x, h2Img - y), (width, h2Img - height), (255, 0, 0), 1) # xy base, wh. color, thickness
#     cv2.putText(img2, a[0], (x, h2Img - y + 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

# for a in box3.splitlines(): # converts string of values into a list of values
#     a = a.split()
#     x, y = int(a[1]), int(a[2])
#     width, height = int(a[3]), int(a[4])

#     cv2.rectangle(img3, (x, h3Img - y), (width, h3Img - height), (255, 0, 0), 1) # xy base, wh. color, thickness
#     cv2.putText(img3, a[0], (x, h3Img - y + 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

# word boxes: how is this done?
for z, a in enumerate(data1.splitlines()):
    if z != 0:
        a = a.split()
        if len(a) == 12:
            x, y = int(a[6]), int(a[7])
            width, height = int(a[8]), int(a[9])
            cv2.rectangle(img1, (x, y), (x + width, y + height), (255, 0, 0), 1)
            cv2.putText(img1, a[11], (x, y + 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

for z, a in enumerate(data2.splitlines()):
    if z != 0:
        a = a.split()
        if len(a) == 12:
            x, y = int(a[6]), int(a[7])
            width, height = int(a[8]), int(a[9])
            cv2.rectangle(img2, (x, y), (x + width, y + height), (255, 0, 0), 1)
            cv2.putText(img2, a[11], (x, y + 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

for z, a in enumerate(data3.splitlines()):
    if z != 0:
        a = a.split()
        if len(a) == 12: # standard word array length attributes?
            x, y = int(a[6]), int(a[7])
            width, height = int(a[8]), int(a[9])
            cv2.rectangle(img3, (x, y), (x + width, y + height), (255, 0, 0), 1)
            cv2.putText(img3, a[11], (x, y + 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

cv2.imshow('image 1', img1)
cv2.imshow('image 2', img2)
cv2.imshow('image 3', img3)
cv2.waitKey(0) # 0: still img, 1: img for 1ms only, etc.
















# tesseract problem: reading both black and white text?
# cannot read the knots and direction number within block..
# may need to do image enhancements / modifications for each frame
# why can't it grab this bigger white numbers when all the others are the same? is there a way to subsection the image for text grabbing without creating new image files?


# get frame and import into pillow, export binarized image, then push to opencv? pillow can go through tesseract too...

# maybe use open cv to create the frame from screen recording, then utilize pillow for use


# move onto screen recorder, see if it is possible to screen record singular application / size of screen