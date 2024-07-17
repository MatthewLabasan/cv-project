import cv2
from PIL import ImageGrab # from pillow
import numpy as np

height = 1028
width = 1028

# video encoding
fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v") # choose a video type
captured_video = cv2.VideoWriter("recorded_video.mp4", fourcc, 30.0, (height, width)) # title of video, format, fps, height and width of screen

while True:
    # modify last two numbers to simplify where the gui is captured
    img = ImageGrab.grab(bbox = (0, 0, height, width)) # first two are top right corner, then height width

    # put img into np array: holds rgb information for each pixel. form is (H, W, Channel)
    np_img = np.array(img)

    # change color of image to rgb format
    cvt_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB)

    # expects image data in np array form
    cv2.imshow("Video Capture", cvt_img)

    # write to video
    captured_video.write(cvt_img)

    # waits for 20ms. if a key is pressed matching ascii 27 (esc key), loop breaks
    key = cv2.waitKey(20)
    if key == 27:
        break

cv2.destroyAllWindows