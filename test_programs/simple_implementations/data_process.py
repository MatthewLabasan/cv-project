import cv2
import pytesseract # ocr module
from PIL import ImageGrab # from pillow
import numpy as np
from datetime import date
import asyncio
import os
from screeninfo import get_monitors # works well on windows, not macOS


# don't need line below as long as you set up a virtual env and reinstall requirements and tesseract. not sure how to do tesseract on windows yet!
# use path to tesseract executable. to find this on mac: `which tesseract`. to find this on windows: `where tesseract``
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

img = cv2.imread('./test_images/sandIslandTest2OG.png')
print("img: \n" + pytesseract.image_to_string(img) + "\n") 

# format of image_to_data (attributes of each data object)
# level	  page_num	  block_num	  par_num	line_num	word_num	left(x)	  top(y)  width	height	confidence	text
data = pytesseract.image_to_data(img)

for index, data_array in enumerate(data.splitlines()): # iterate through data. enumerate returns a tuple of index and array of data
    if index != 0: # ignore first object
        data_array = data_array.split()
    if len(data_array) == 12: # standard word array attribute length: verifies we parse a identified word
        print(f"{index}: x={data_array[6]}, y={data_array[7]}, confidence={data_array[10]}, word={data_array[11]}")

# store data in csv as: 
# X: Time, Lat(deg), Lon(deg), Satellites, Uncertainty(m), Motor Speed, OCB Temp(C), Runtime(min), Charge(%), Voltage(V), Current(A), Power(W), Stator Temp(C), PCB Temp(C), Fields with <80% Certainty
# INSERT INTO FOR LOOP

# to make easier to write data to csv
    # could sort array of arrays to be in chunks of arrays. ex. one array is 200-210 y value.
    # this takes up extra space, but we just parse through it once o(n), though, we can't guarentee the y-axis size difference.
    # we need to be able to compare the KEY word's y value with y values outside.
    # maybe in line 26, check each if KEY word is inside a dictionary of predefined values. if is the value, grab key (y) and store, else if it is similar (can use sequence manager (O(n*m), so kinda slow but might be fine for this since its only a couple thousand comparisons with SHORT strings), then replace with the actual key and grab the value.
        # https://datascience.stackexchange.com/questions/20536/how-to-improve-ocr-scanning-results
    # go through each one again, checking for similar y values using math.isclose
    # if it is close, push data to that column, specifically matching the date value!!!

    # sort csv file at the end by date


    # psuedocode