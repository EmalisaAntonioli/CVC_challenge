import csv
import cv2
from mss import mss
import numpy as np
import time
import uuid
import pygame
import os

# Set up game area (full screen)
game_area = {"left": 0, "top": 0, "width": 1920, "height": 1080}
capture = mss()

# Ensure the screen capture directory exists
os.makedirs('screen_caps', exist_ok=True)

# Initialize Pygame and Joystick
pygame.init()
pygame.joystick.init()

# Assuming one joystick (PS4 controller) is connected
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Detected controller: {joystick.get_name()}")
else:
    print("No joystick detected!")
    exit(1)

def collect_controller_data():
    pygame.event.pump()  # Process event queue to get the latest controller state

    # Capture axis values for the PS4 controller
    left_stick_x = joystick.get_axis(0)  # Left stick X-axis
    left_stick_y = joystick.get_axis(1)  # Left stick Y-axis
    right_stick_x = joystick.get_axis(2)  # Right stick X-axis
    right_stick_y = joystick.get_axis(3)  # Right stick Y-axis
    trigger_left = joystick.get_axis(4)   # L2 Trigger
    trigger_right = joystick.get_axis(5)  # R2 Trigger

    # Capture button presses (0: cross, 1: circle, 2: square, etc.)
    button_cross = joystick.get_button(0)
    button_circle = joystick.get_button(1)
    button_square = joystick.get_button(2)
    button_triangle = joystick.get_button(3)

    # Return the joystick state as a dictionary or tuple
    return {
        "left_stick_x": left_stick_x,
        "left_stick_y": left_stick_y,
        "right_stick_x": right_stick_x,
        "right_stick_y": right_stick_y,
        "trigger_left": trigger_left,
        "trigger_right": trigger_right,
        "button_cross": button_cross,
        "button_circle": button_circle,
        "button_square": button_square,
        "button_triangle": button_triangle
    }

# Open a CSV file to log controller data
with open('controller_log.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Left Stick X", "Left Stick Y", "Right Stick X", "Right Stick Y", "Trigger Left", "Trigger Right", "Cross", "Circle", "Square", "Triangle"])

    def collect_gameplay():
        # Capture screen image
        gamecap = np.array(capture.grab(game_area))

        # Save the screenshot
        filename = f'screen_caps/{uuid.uuid1()}.jpg'
        cv2.imwrite(filename, gamecap)

        # Get controller data
        controller_data = collect_controller_data()
        timestamp = time.time()

        # Write controller data to CSV
        writer.writerow([
            timestamp,
            controller_data["left_stick_x"],
            controller_data["left_stick_y"],
            controller_data["right_stick_x"],
            controller_data["right_stick_y"],
            controller_data["trigger_left"],
            controller_data["trigger_right"],
            controller_data["button_cross"],
            controller_data["button_circle"],
            controller_data["button_square"],
            controller_data["button_triangle"]
        ])

        # Optionally flush to ensure data is saved periodically
        file.flush()

if __name__ == '__main__':
    # Allow some time to open the game
    time.sleep(2)

    while True:
        collect_gameplay()

        # Control capture speed to avoid overloading (optional)
        time.sleep(0.1)  # Capture approximately 10 frames per second
