import cv2
from mss import mss
import numpy as np
import time
import uuid
import pyvjoy
import os

# Create directory for saving screenshots and inputs
if not os.path.exists('screen_caps'):
    os.makedirs('screen_caps')

# ScreenCapture class for handling screen capture
class ScreenCapture:
    def __init__(self, game_area=None):
        self.capture = mss()
        if game_area is None:
            monitor = self.capture.monitors[1]  # Use primary monitor
            self.game_area = {"left": 0, "top": 0, "width": monitor["width"], "height": monitor["height"]}
        else:
            self.game_area = game_area

    def capture_frame(self):
        gamecap = np.array(self.capture.grab(self.game_area))
        return gamecap

    def save_frame(self, frame, timestamp):
        filename = f'screen_caps/{timestamp}.jpg'
        cv2.imwrite(filename, frame)


# JoystickHandler class for managing joystick inputs
class JoystickHandler:
    def __init__(self, device_id=1):
        self.vjoy_device = pyvjoy.VJoyDevice(device_id)

    def get_joystick_input(self):
        # TODO adjust this in accordance with everything that needs to be tracked
        x_axis = self.vjoy_device.get_axis(pyvjoy.HID_USAGE_X)
        y_axis = self.vjoy_device.get_axis(pyvjoy.HID_USAGE_Y)
        return {"X": x_axis, "Y": y_axis}

    def save_joystick_input(self, joystick_input, timestamp):
        filename = f'screen_caps/{timestamp}.txt'
        with open(filename, 'w') as f:
            f.write(f"X-Axis: {joystick_input['X']}\n")
            f.write(f"Y-Axis: {joystick_input['Y']}\n")


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
            joystick_input = self.joystick_handler.get_joystick_input()
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
