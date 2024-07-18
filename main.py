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
from screeninfo import get_monitors # works well on windows, not macOS

async def python_ocr(img):
    # don't need line below as long as you set up a virtual env and reinstall requirements and tesseract. not sure how to do tesseract on windows yet!
    # use path to tesseract executable. to find this on mac: `which tesseract`. to find this on windows: `where tesseract``
    
    pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
    print("img: \n" + pytesseract.image_to_string(img) + "\n") 

async def capture():
    ocr_tasks = []

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

    # csv file creation (TO DO)

    # capture video (1fps)
    while True:
        # capture image
        img = ImageGrab.grab(bbox = (0, 0, width, height)) # first two are top right corner, then height width -> try no params on windows for full screen (supported)

        # push image to ocr for async analysis
        np_img = np.array(img) # put img into np array: holds rgb information for each pixel. form is (H, W, Channel)
        ocr_tasks.append(python_ocr(np_img))

        # create video
        cvt_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB) # change color of image to rgb format
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

    # await csv creation
    await asyncio.gather(*ocr_tasks)
    print("CSV file created successfully")

def main():
    asyncio.run(capture())

if __name__ == "__main__":
    main()