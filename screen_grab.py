import cv2
from mss import mss
import numpy as np
import time
import uuid
# import pyvjoystick as pyvjoy
import os
import pygetwindow as gw
from inputs import get_gamepad
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

    def save_frame(self, frame, timestamp):
        filename = f'screen_caps/{timestamp}.jpg'
        cv2.imwrite(filename, frame)

    def get_game_window_coords(self, title="Forza Horizon 4"):
        game_window = gw.getWindowsWithTitle(title)
        if game_window:
            game_window = game_window[0]
            return game_window.left, game_window.top, game_window.width, game_window.height
        return None


# JoystickHandler class for managing joystick inputs
class JoystickHandler:
    def __init__(self, device_id=1):
        self.gamepad_state = {"LX": 0, "LY": 0, "RX": 0, "RY": 0, "RT": 0, "LT": 0}


    # Initialize gamepad state

    def get_gamepad_events(self):
        events = get_gamepad()
        for event in events:
            if event.ev_type == "Absolute":
                if event.code == "ABS_X":  # Left stick X-axis
                    self.gamepad_state["LX"] = event.state
                elif event.code == "ABS_Y":  # Left stick Y-axis
                    self.gamepad_state["LY"] = event.state
                elif event.code == "ABS_RX":  # Right stick X-axis
                    self.gamepad_state["RX"] = event.state
                elif event.code == "ABS_RY":  # Right stick Y-axis
                    self.gamepad_state["RY"] = event.state
                elif event.code == "ABS_RZ":  # Right trigger
                    self.gamepad_state["RT"] = event.state
                elif event.code == "ABS_Z":  # Left trigger
                    self.gamepad_state["LT"] = event.state

    def save_gamepad_events(self):
        with open('controller_log.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Left Stick X", "Left Stick Y", "Right Stick X", "Right Stick Y", "Trigger Left", "Trigger Right"])

            
        return NotImplementedError


# GameSession class to handle the overall session
class GameSession:
    def __init__(self, screen_capture, joystick_handler):
        self.screen_capture = screen_capture
        self.joystick_handler = joystick_handler

    def run(self, duration=60):
        start_time = time.time()
        while time.time() - start_time < duration:
            # Generate a timestamp for synchronization
            timestamp = str(uuid.uuid1())  # Generates a unique identifier for each frame/input set

            # Capture the game screen
            frame = self.screen_capture.capture_frame()
            self.screen_capture.save_frame(frame, timestamp)

            # Capture joystick inputs
            joystick_input = self.joystick_handler.process_gamepad_events()
            self.joystick_handler.save_joystick_input(joystick_input, timestamp)

            # Optional: Add a small delay to prevent overwhelming the system
            time.sleep(0.1)


if __name__ == '__main__':
    # Allow time to start the game
    time.sleep(2)

    # Create the components
    screen_capture = ScreenCapture()
    joystick_handler = JoystickHandler()

    # Start a game session for 60 seconds
    session = GameSession(screen_capture, joystick_handler)
    session.run(duration=60)
