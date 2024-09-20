import cv2
from mss import mss
import numpy as np
import time
import uuid

# use cv2.selectROI instead?
# adjust the game area as required
game_area = {"left": 0, "top": 0, "width": 1920, "height": 1080}
capture = mss()
def collect_frames():
    gamecap = np.array(capture.grab(game_area))
    filename = f'screen_caps/{uuid.uuid1()}.jpg'
    cv2.imwrite(filename, gamecap)

if __name__ == '__main__':
    # give yourself enough sleep time to open and start the game
    time.sleep(2)
    while True:
        collect_frames()