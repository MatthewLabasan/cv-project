import cv2 # open cv module
import pytesseract # ocr module
from PIL import Image # pillow: image processing
import numpy as np

# don't need line below as long as you set up a virtual env and reinstall requirements and tesseract. not sure how to do tesseract on windows yet!

# use path to tesseract executable. to find this on mac: `which tesseract`. to find this on windows: `where tesseract``
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# OPEN CV
# load the frame
img1 = cv2.imread('./test_images/sandIslandTest1_live.png')
img2 = cv2.imread('./test_images/GUI.png')
img3 = cv2.imread('./test_images/halfscreen.png')

# processing recommendations: rescale
img1 = cv2.resize(img1, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
# grayscale
img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
# dilation and erosion to remove noise (done on binary images)
kernel = np.ones((2, 2), np.uint8) # erodes to be white only if all pixels within array size is 1
img3 = cv2.dilate(img3, kernel, iterations=1)
img3 = cv2.erode(img3, kernel, iterations=1)
# thershold to binary
cv2.threshold(img3, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# show the frame
# cv2.imshow('image 1', img1)
# cv2.imshow('image 2', img2)
# cv2.imshow('image 3', img3)

cv2.waitKey(1000) # 0: still img, 1: img for 1ms only, etc.

# detect text on img
print("img1: \n" + pytesseract.image_to_string(img1) + "\n")
print("img2: \n" + pytesseract.image_to_string(img2) + "\n")
print("img3: \n" + pytesseract.image_to_string(img3) + "\n")


# PILLOW














# tesseract problem: reading both black and white text?
# cannot read the knots and direction number within block..
# may need to do image enhancements / modifications for each frame
# why can't it grab this bigger white numbers when all the others are the same? is there a way to subsection the image for text grabbing without creating new image files?


# get frame and import into pillow, export binarized image, then push to opencv? pillow can go through tesseract too...

# maybe use open cv to create the frame from screen recording, then utilize pillow for use


# move onto screen recorder, see if it is possible to screen record singular application / size of screen