import cv2
import pytesseract
from PIL import ImageGrab 
import numpy as np
from datetime import date, datetime
import asyncio
import os
# import csv
# import threading
# import time
from screeninfo import get_monitors # works better on windows
import pandas as pd

# csv_lock = threading.Lock()
txt_file_name = "./data_log/%s.txt" % date.today()

async def python_ocr(img, txt_file_name):
    data = pytesseract.image_to_string(img)
    time = datetime.now().strftime('%H:%M:%S')

    with open(txt_file_name, 'a') as file:
        file.write(f"========================{datetime.now().strftime('%H:%M:%S')}=========================\n\n{data}\n\n")
   
# async def append_to_csv(filename, dataframe):
#     # use the lock. prevents more than one thread appending at once
#     with csv_lock:
#         dataframe.to_csv(filename, mode='a', index=False, header=False)

async def capture():
    # get dimensions of screen
    for m in get_monitors():
        width = m.width
        height = m.height
    screen_size = (width, height) # or modify to specific section

    # video encoding & saving
    if not os.path.exists('./screen_recordings'):
        os.makedirs('./screen_recordings')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    captured_video = cv2.VideoWriter('./screen_recordings/%s.mp4' % date.today(), fourcc, 1.0, screen_size, True)

    # create csv file. create here to prevent race issues
    # csv_file_name = "./data_log/%s.csv" % date.today()
    # if not os.path.exists(csv_file_name):
    #     csv_headers = ["time" "lat(deg)", "lat", "lon", "lon(deg)", "satellites", "uncertainty(m)", "charge", "hlc", "srr"] # lowercase, similarity max 50%
    #     with open(csv_file_name, 'w') as csv_file:
    #         csv_writer = csv.writer(csv_file, delimiter=',')
    #         csv_writer.writerow(csv_headers)

    # create txt file
    if not os.path.exists(f'./data_log/{txt_file_name}'):
        with open(txt_file_name, 'w') as file:
            pass

    print("Screen capture successfully started.")

    # capture video (1fps)
    while True:
        # capture image
        print("Recording...")
        img = ImageGrab.grab(bbox = (0, 0, width, height))

        # push image to ocr for async analysis and csv creation
        np_img = np.array(img)
        await python_ocr(np_img, txt_file_name)

        # create video
        cvt_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB) # change color to rgb format
        cv2.imshow("Video Capture", cvt_img)
        captured_video.write(cvt_img)

        # exit function
        key = cv2.waitKey(1000)
        if key == 27:
            break

    # finialize video
    captured_video.release
    cv2.destroyAllWindows
    print("Video and txt file successfully saved.")

def main():
    asyncio.run(capture())


if __name__ == "__main__":
    main()