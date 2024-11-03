import cv2
from mss import mss
import numpy as np
import time
import os
import pygetwindow as gw
import csv
import pygame

# Create directory for saving screenshots
if not os.path.exists('screen_caps'):
    os.makedirs('screen_caps')

class ScreenCapture:
    """Handle taking screen captures of the game"""
    def __init__(self, game_area=None):
        self.capture = mss() 
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

class JoystickHandler:
    """JoystickHandler class for managing joystick inputs"""
    def __init__(self):
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
        
        # Process event queue
        pygame.event.pump()  
        
        # Update stick and trigger values
        self.gamepad_state["LX"] = self.joystick.get_axis(0)  # Left Stick X-axis
        self.gamepad_state["LT"] = self.joystick.get_axis(4)  # Left Trigger
        self.gamepad_state["RT"] = self.joystick.get_axis(5)  # Right Trigger

        return self.gamepad_state

class GameSession:
    """GameSession class to handle the overall session"""
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
