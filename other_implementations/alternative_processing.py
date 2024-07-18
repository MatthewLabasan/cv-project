import cv2
import pytesseract # ocr module
from PIL import ImageGrab # from pillow
import numpy as np
import pandas as pd
from datetime import date, datetime
import asyncio
import os
import math
import csv
from screeninfo import get_monitors # works well on windows, not macOS
from rapidfuzz import fuzz

# This file is an attempt to cleanly recognize and save extracted text to a CSV file. Due to time constraints and issues with debugging, it has not yet been implemented.

pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

img = cv2.imread('./test_images/desired2.png')
print("img: \n" + pytesseract.image_to_string(img) + "\n") 
time = datetime.now().strftime('%H:%M:%S')

# instantiate data structures for comparison
headers = ["lat", "lon", "satellites", "uncertainty(m)", "charge", "hlc", "srr"] # lowercase, similarity max 50%
header_y = {}
csv_headers = ["time", "lat", "lon", "satellites", "uncertainty(m)", "charge", "hlc", "srr"] # lowercase, similarity max 50%

# create pandas data frame table to be appended to already made csv
df = pd.DataFrame(columns=csv_headers)
df.loc[0,"time"] = time


# format of image_to_data (attributes of each data object)
# level	  page_num	  block_num	  par_num	line_num	word_num	left(x)	  top(y)  width	height	confidence	text
data = pytesseract.image_to_data(img)

# identify header y-coordinates
for index, data_array in enumerate(data.splitlines()): # iterate through data. enumerate returns a tuple of index and array of data. note that splitlines does not modify in place
    if index != 0: # ignore first object
        data_array = data_array.split()
    if len(data_array) == 12: # standard array length
        print(data_array)
        for word in headers:
            if fuzz.ratio(data_array[11].lower(), word) >= 70.0:
                header_y[int(data_array[7])] = word
    # time complexity: run through image array (n) * 9 comparisons in header = o(n)

# go through each again, append to corresponding header
for index, data_array in enumerate(data.splitlines()):
    if index != 0:
        data_array = data_array.split()
    if len(data_array) == 12:
        print(data_array)
        for key in header_y.keys():
            print(f"int(data_array[7] = {int(data_array[7])}, key = {key})")
            if math.isclose(int(data_array[7]), key, abs_tol=10): # if y coord is same,
                df.loc[0, header_y[key]] = data_array[11] 
                print("updated")


# PROBLEM: VALUES WITH SIMILAR Y'S (COORDS, SATELLITES), ETC.

        # print(f"{index}: x={data_array[6]}, y={data_array[7]}, confidence={data_array[10]}, word={data_array[11]}")
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns
print(df)
print(header_y.keys())
print(header_y.values())
# return df