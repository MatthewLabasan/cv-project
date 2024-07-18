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


# don't need line below as long as you set up a virtual env and reinstall requirements and tesseract. not sure how to do tesseract on windows yet!
# use path to tesseract executable. to find this on mac: `which tesseract`. to find this on windows: `where tesseract``
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












# purpose of program: screen record data for future reference and automate data collection with optical character recognition

# write screen recorder

# for every frame read, push into tesseract and append to txt file
# write to video

# this assumes that it will take only a second to complete the tesseract. how can we prevent script from holding up (as it will probably take longer, alongside data sorting and identification)?
# try to ptimize tesseract by reducing image changes and reducing scan size (decrease size to gui only)

# possible solutions: 
    # place images into an array/stack or something, and process data after.
    # utilize an async module in python (asyncio) and push the tesseracts to the side.
        # depends if we want to analyze while running or analyze after running.
    # record data every 5 or so seconds instead

import cv2
import pytesseract # ocr module
from PIL import ImageGrab # from pillow
import numpy as np
from datetime import date
import asyncio
import os
import csv
import threading
import time
from screeninfo import get_monitors # works well on windows, not macOS

import pandas as pd

csv_lock = threading.Lock()

async def python_ocr(img, csv_file_name):
    # don't need line below as long as you set up a virtual env and reinstall requirements and tesseract. not sure how to do tesseract on windows yet!
    # use path to tesseract executable. to find this on mac: `which tesseract`. to find this on windows: `where tesseract``
    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract" # don't need this if tesseract is added to PATH (done at installation)
    print("img: \n" + pytesseract.image_to_string(img) + "\n") 

    # format of image_to_data (attributes of each data object)
    # level	  page_num	  block_num	  par_num	line_num	word_num	left(x)	  top(y)  width	height	confidence	text
    # would like to extract left [6] and top [7], and also record confidence for fun
    data = pytesseract.image_to_data(img)

    for index, data_array in enumerate(data.splitlines()): # iterate through data. enumerate returns a tuple of index and array of data
        if index != 0: # ignore first object
            data_array = data_array.split()
        if len(data_array) == 12: # standard word array attribute length: verifies we parse a identified word
            print(f"{index}: x={data_array[6]}, y={data_array[7]}, confidence={data_array[10]}, word={data_array[11]}")

    # CALL APPEND_TO_CSV, NOW WE CAN HANDLE ASYCN OCRS AND THREAD LOCK APPENDS

async def append_to_csv(filename, dataframe):
    # use the lock. prevents more than one thread appending at once
    with csv_lock:
        dataframe.to_csv(filename, mode='a', index=False, header=False)

def capture():
    # get dimensions of screen
    for m in get_monitors():
        width = m.width # accesible outside; no block-level scope
        height = m.height
    screen_size = (width, height) # or modify to specific section

    # video encoding & saving
    if not os.path.exists('./screen_recordings'):
        os.makedirs('./screen_recordings')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    captured_video = cv2.VideoWriter('./screen_recordings/%s.mp4' % date.today(), fourcc, 1.0, screen_size, True)

    # create csv file. create here to prevent race issues
    csv_file_name = "./csv_files/%s.csv" % date.today()
    if not os.path.exists(csv_file_name):
        csv_headers = ["time" "lat(deg)", "lat", "lon", "lon(deg)", "satellites", "uncertainty(m)", "charge", "hlc", "srr"] # lowercase, similarity max 50%
        with open(csv_file_name, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(csv_headers)

    print("Screen capture successfully started.")

    # capture video (1fps)
    while True:
        # capture image
        print("Recording...")
        img = ImageGrab.grab(bbox = (0, 0, width, height)) # first two are top right corner, then height width -> try no params on windows for full screen (supported)

        # push image to ocr for async analysis and csv creation
        np_img = np.array(img) # put img into np array: holds rgb information for each pixel. form is (H, W, Channel)
        python_ocr(np_img, csv_file_name) # process data async

        # create video
        cvt_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB) # change color of image to rgb format
        # THIS WINDOW IS NEEDED TO REGISTER WAITKEY. ELSE UTILIZE A KEY REGISTER LIBRARY
        cv2.imshow("Video Capture", cvt_img) # expects image data in np array form
        captured_video.write(cvt_img)

        # exit function
        key = cv2.waitKey(1000) # returns ascii of key pressed or -1 if none
        if key == 27:
            break

    # finialize video
    captured_video.release
    cv2.destroyAllWindows
    print("Video successfully saved. Awaiting CSV file creation.")

def main():
    capture()

    # ensure async loop is empty and csv is complete
    while asyncio.get_event_loop():
        time.sleep(5)
        print("CSV file still processing...")

    # sort csv file

    print("CSV file created successfully")
    


if __name__ == "__main__":
    # main()

    df = pd.DataFrame(columns=['hello', 'hi'])
    print(df)