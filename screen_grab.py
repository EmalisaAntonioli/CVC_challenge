import PIL.ImageShow
import cv2
from mss import mss
import numpy as np
import time
import uuid
import os
import pygetwindow as gw
from inputs import get_gamepad
import csv
import pygame
import re


# Create directory for saving screenshots and inputs
if not os.path.exists('screen_caps'):
    os.makedirs('screen_caps')
    # os.makedirs('screen_caps/train/steer_right')
    # os.makedirs('screen_caps/train/brake')
    # os.makedirs('screen_caps/train/gas')

# ScreenCapture class for handling screen capture
class ScreenCapture:
    def __init__(self, game_area=None):
        self.capture = mss()  # Correct mss initialization
        if game_area is None:
            game_area = self.get_game_window_coords()
            if game_area is None:
                raise ValueError("Game window not found.")
            self.game_area = {
                "left": game_area[0], 
                "top": game_area[1], 
                "width": game_area[2], 
                "height": game_area[3]
            }
        else:
            self.game_area = game_area

    def capture_frame(self):
        frame = np.array(self.capture.grab(self.game_area))
        return frame

    def save_frame(self, frame, name):
        # Regular expression pattern
        # pattern = r'(?P<timestamp>[0-9a-fA-F\-]+)_(?P<LX>[0-9\.-]+)_(?P<LT>[0-9\.-]+)_(?P<RT>[0-9\.-]+)$'
        # print(name)

        # # Search for the pattern in the string
        # match = re.search(pattern, name)

        # if match:
        #     # Extracting named groups
        #     timestamp = match.group('timestamp')
        #     LX = float(match.group('LX'))
        #     LT = float(match.group('LT'))
        #     RT = float(match.group('RT'))

        #     if LX > 0.1:
        #         filename = f'sreen_caps/train/steer_right/{name}.jpg'
        #         cv2.imwrite(filename, frame)
        #     elif LX < -0.1:
        #         filename = f'screen_caps/train/steer_left/{name}.jpg'
        #         cv2.imwrite(filename, frame)
        #     elif LT > 0.1:
        #         filename = f'screen_caps/train/brake/{name}.jpg'
        #         cv2.imwrite(filename, frame)
        #     elif RT > 0.1:
        #         filename = f'screen_caps/train/gas/{name}.jpg'
        #         cv2.imwrite(filename, frame)

        #     print("Timestamp:", timestamp)
        #     print("LX:", LX)
        #     print("LT:", LT)
        #     print("RT:", RT)
        # else:
        #     print("No match found.")
        print(name)
        filename = f'screen_caps/{name}.jpg'
        cv2.imwrite(filename, frame)


    def get_game_window_coords(self, title="Forza Horizon 4"):
        game_window = gw.getWindowsWithTitle(title)
        if game_window:
            game_window = game_window[0]
            return game_window.left, game_window.top, game_window.width, game_window.height
        return None
    
    def resize_frame(self, frame):
        # Cut top 30% off the frame, to reduce distractions        
        # Get the dimensions of the image
        height, width, _ = frame.shape
        
        # Calculate the height to cut off
        cut_height = int(height * 0.30)

        # Cut the image by slicing the array
        cropped_frame = frame[cut_height:height, 0:width]  # Cuts off the top part

        return cropped_frame



# JoystickHandler class for managing joystick inputs
class JoystickHandler:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.joystick.init()
        
        # Check if a controller is connected
        if pygame.joystick.get_count() == 0:
            raise Exception("No joystick/gamepad connected.")
        
        # Initialize the first connected joystick
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        # Initialize gamepad state
        self.gamepad_state = {
            "LX": 0,  # Left Stick X-axis
            "RT": 0,  # Right Trigger (treated as an axis)
            "LT": 0   # Left Trigger (treated as an axis)
        }

        # Open CSV file to store gamepad input data
        self.csv_file = open('controller_log.csv', 'a', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        
        # Write CSV header
        self.csv_writer.writerow(["Timestamp", "Left Stick X", "Left Stick Y", "Right Stick X", "Right Stick Y", "Trigger Left", "Trigger Right"])

    def get_gamepad_events(self):
        """Poll gamepad events and update the gamepad state."""
        pygame.event.pump()  # Process event queue
        
        # Update stick and trigger values
        self.gamepad_state["LX"] = self.joystick.get_axis(0)  # Left Stick X-axis
        self.gamepad_state["LT"] = self.joystick.get_axis(4)  # Left Trigger
        self.gamepad_state["RT"] = self.joystick.get_axis(5)  # Right Trigger

        return self.gamepad_state


# GameSession class to handle the overall session
class GameSession:
    def __init__(self, screen_capture, joystick_handler):
        self.screen_capture = screen_capture
        self.joystick_handler = joystick_handler

    def run(self, duration=60):
        start_time = time.time()
        while time.time() - start_time < duration:
            
            # Capture joystick inputs
            joystick_input = self.joystick_handler.get_gamepad_events()

            # Generates a unique identifier for each frame/input set
            timestamp = time.strftime("%Y%m%d_%H%M%S")

            # Capture the game screen
            frame = self.screen_capture.capture_frame()

            # Resize the game screen
            frame = self.screen_capture.resize_frame(frame)

            # The name will now look like timestamp_joystickLX_joystickLT_joystickRT
            screen_capture_name = f'{timestamp}_{round(joystick_input["LX"],4)}_{round(joystick_input["LT"],4)}_{round(joystick_input["RT"],4)}'

            self.screen_capture.save_frame(frame, screen_capture_name)

            # Adjust to change how many caps are taken
            time.sleep(0.5)
        # self.joystick_handler.close_csv()


if __name__ == '__main__':
    # Allow time to start the game
    time.sleep(10)
    print("start")
    time.sleep(2)
    # Create the components
    screen_capture = ScreenCapture()
    joystick_handler = JoystickHandler()

    # Start a game session for 600 seconds
    session = GameSession(screen_capture, joystick_handler)
    session.run(duration=600)
