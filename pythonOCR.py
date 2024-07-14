import cv2 # open cv module
import pytesseract # ocr module

# don't need line below as long as you set up a virtual env and reinstall requirements and tesseract. not sure how to do tesseract on windows yet!

# use path to tesseract executable. to find this on mac: `which tesseract`. to find this on windows: `where tesseract``
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# load the frame
img1 = cv2.imread('./test_images/sandIslandTest1_live.png')
img2 = cv2.imread('./test_images/GUIcircles.png')
img3 = cv2.imread('./test_images/GUI.png')

# show the frame
cv2.imshow('image 1', img1)
cv2.imshow('image 2', img2)
cv2.imshow('image 3', img3)

cv2.waitKey(1) # 0: still img, 1: img for 1ms only, etc.

# detect text on img
print("img1: \n" + pytesseract.image_to_string(img1) + "\n")
print("img2: \n" + pytesseract.image_to_string(img2) + "\n")
print("img3: \n" + pytesseract.image_to_string(img3) + "\n")

# tesseract problem: reading both black and white text?
# cannot read the knots and direction number within block..
# may need to do image enhancements / modifications for each frame
# why can't it grab this bigger white numbers when all the others are the same? is there a way to subsection the image for text grabbing without creating new image files?