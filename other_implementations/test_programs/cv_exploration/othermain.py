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
import re

csv_lock = threading.Lock()
csv_file_name = "./csv_files/%s.csv" % date.today()

async def python_ocr(img):
    # don't need line below as long as you set up a virtual env and reinstall requirements and tesseract. not sure how to do tesseract on windows yet!
    # use path to tesseract executable. to find this on mac: `which tesseract`. to find this on windows: `where tesseract``
    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract" # don't need this if tesseract is added to PATH (done at installation)
    data = await pytesseract.image_to_string(img)

    start_marker = "Lat"
    end_marker = "PCB Temp"
    start_index = data.find(start_marker)
    end_index = data.find(end_marker, start_index) + len(end_marker)

    trimmed_data = data[start_index:end_index].strip()

    # Create DataFrame from the trimmed string
    try:
        df = extract_and_create_dataframe(trimmed_data)
        await append_to_csv(csv_file_name, df)
    except ValueError as e:
        print(f"Error: {e}")

def extract_and_create_dataframe(data_string):
    # Use regular expressions to extract the desired portion of the string
    match = re.search(r'Lat.*?PCB Temp.*', data_string, re.DOTALL)
    if match:
        extracted_data = match.group(0)
    else:
        raise ValueError("Couldn't find matching data in the string.")

    # Split the extracted string into lines and then into key-value pairs
    items = extracted_data.splitlines()

    # Initialize an empty dictionary to store extracted data
    data_dict = {}

    # Process key-value pairs
    for line in items:
        if line.strip():  # Skip empty lines
            parts = line.split()
            key = ' '.join(parts[:-1])  # Combine all parts except the last one as key
            value = parts[-1]  # Last part as value

            # Special case for Charge (%) to format values as "80.0, 79.0"
            if "Charge (%)" in key:
                value = ', '.join(parts[-2:])  # Join the last two parts with comma

            data_dict[key] = value

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame([data_dict])

    return df

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
        python_ocr(np_img) # process data async

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
    main()