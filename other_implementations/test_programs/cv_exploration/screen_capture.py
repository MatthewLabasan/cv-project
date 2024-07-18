import cv2
from PIL import ImageGrab # from pillow
import numpy as np
from screeninfo import get_monitors # works well on windows, not macOS

height = 0
width = 0

# get dimensions of screen
for m in get_monitors():
    width = m.width
    height = m.height
    print(m)

screen_size = (width, height)

# video encoding
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # choose a video type. * unpacks string into separate char args
captured_video = cv2.VideoWriter("./screen_recordings/recorded_video.mp4", fourcc, 1.0, screen_size, True) # title of video, format, fps, width and height of screen, color

while True:
    # modify last two numbers to simplify where the gui is captured
    img = ImageGrab.grab(bbox = (0, 0, width, height)) # first two are top right corner, then height width

    # img = ImageGrab.grab() # full screen -> use with mac testing, but should be fine in windows pc

    # put img into np array: holds rgb information for each pixel. form is (H, W, Channel)
    np_img = np.array(img)

    # change color of image to rgb format
    cvt_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB)

    # expects image data in np array form
    cv2.imshow("Video Capture", cvt_img)

    # write to video
    captured_video.write(cvt_img)

    # waits for 1s. if a key is pressed matching ascii 27 (esc key), loop breaks. otherwise, take next photo
    key = cv2.waitKey(1000) # returns ascii of key pressed or -1 if none
    if key == 27:
        break

captured_video.release
cv2.destroyAllWindows