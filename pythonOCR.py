import cv2 # open CV module
import pytesseract

# notice that as long as we change interpreter to conda, it will work

# don't need in downloaded program as long as you set up a virtual env and reinstall requirements
pytesseract.pytesseract.tesseract_cmd = "/Users/matthewlabasan/anaconda3/lib/python3.11/site-packages/pytesseract"
