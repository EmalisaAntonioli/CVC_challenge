import cv2
from mss import mss
import numpy as np
import time
import uuid
import os
import pygetwindow as gw
import pygame
import csv

# Create directory for saving screenshots and inputs
if not os.path.exists('screen_caps'):
    os.makedirs('screen_caps')

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
        gamecap = np.array(self.capture.grab(self.game_area))
        return gamecap

    def save_frame(self, frame, name):
        filename = f'screen_caps/{name}.jpg'
        cv2.imwrite(filename, frame)

    def get_game_window_coords(self, title="Forza Horizon 4"):
        game_window = gw.getWindowsWithTitle(title)
        if game_window:
            game_window = game_window[0]
            return game_window.left, game_window.top, game_window.width, game_window.height
        return None


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
            "LX": 0,  # Left X-axis
            "LT": 0,  # Left Trigger
            "RT": 0   # Right Trigger
        }

        # Open CSV file for logging joystick data
        self.csv_file = open('joystick_inputs.csv', mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        # Write CSV header
        self.csv_writer.writerow(['timestamp', 'LX', 'LT', 'RT', 'image_name'])

    def get_gamepad_events(self):
        """Poll joystick events and update state."""
        pygame.event.pump()  # Poll for events
        
        # Axis: Left stick (0), Triggers (2:LT, 5:RT)
        self.gamepad_state["LX"] = self.joystick.get_axis(0)
        self.gamepad_state["LT"] = self.joystick.get_axis(2)
        self.gamepad_state["RT"] = self.joystick.get_axis(5)
        
        return self.gamepad_state

    def save_gamepad_events(self, timestamp, image_name):
        """Save joystick state to the CSV file with the image name."""
        self.csv_writer.writerow([
            timestamp,
            self.gamepad_state["LX"],
            self.gamepad_state["LT"],
            self.gamepad_state["RT"],
            image_name
        ])
        # Ensure data is flushed to the CSV file
        self.csv_file.flush()

    def close_csv(self):
        """Close the CSV file properly."""
        self.csv_file.close()


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
            timestamp = str(uuid.uuid1())  

            # Capture the game screen
            frame = self.screen_capture.capture_frame()
            image_name = f'{timestamp}.jpg'
            
            # Save the frame
            self.screen_capture.save_frame(frame, timestamp)

            # Save joystick input data with the image filename
            self.joystick_handler.save_gamepad_events(timestamp, image_name)

            # Adjust to change how many captures are taken (reduce or increase time.sleep)
            time.sleep(0.5)

        self.joystick_handler.close_csv()


if __name__ == '__main__':
    # Allow time to start the game
    time.sleep(10)
    print("start")
    time.sleep(2)
    
    # Create the components
    screen_capture = ScreenCapture()
    joystick_handler = JoystickHandler()

    # Start a game session for 60 seconds
    session = GameSession(screen_capture, joystick_handler)
    session.run(duration=60)