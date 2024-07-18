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
    # we need to be able to compare the key word's y value with y values outside.
    # maybe in line 26, check each if the resulting word is inside an array of predefined values (the headers). if is of good similarity, push y as key and store value (header word) in a new dictionary. (can use sequence manager (O(n*m), so kinda slow but might be fine for this since its only a couple thousand comparisons with SHORT strings OR use fuzzywuzzy ratio), else move on.
        # https://datascience.stackexchange.com/questions/20536/how-to-improve-ocr-scanning-results
        # try to implement early stopping to prevent useless iteration
        # when creating the y value key dictionary, need to create multiple keys (maybe +-2 or 3) that work (increases space usage, but fast indexing and easy implementation) OR
            # once y value key dictionary is created, get keys. when going through each one again, look for similar keys (y values) using the getkeys array. if it is within a certain similarity thershold, access that specific key's value (header) and push data to that header.
                # this might be slower as we are running functions on things that might not even be remotely near a y value key. if we used what is above, we can just index for the key and if its not there, continue.
            # OR we can use a isvalidkey function that loops through getkeys. hold onto that key, and compare to incoming y value. it is within +-5 pixels, return the header needed / take data and add it to that header.
                # same as above alternative. does methods on things we don't need to do.
    # go through each one again, checking for similar y values using math.isclose (or method above)
    # -> will have iterated through array twice = o(n * (p*q) where p*q is small int numbers) + o(n + n * math.isclose run time) -> should be o(n)
    # if it is close, push data to that column, specifically matching the date value!!!

    # improvements: in first run, remove

# improved pseudocode

    # sort csv file at the end by date


    # psuedocode