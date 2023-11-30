import cv2
import numpy as np
import pyautogui
import time
from pynput import mouse
import keyboard
import math

# Path to the file with the mole
template_path = 'Mole.png'

# Set the value for the treshold for the image detection
threshold = 0.80
double_click_threshold = 30  # We set this in order to do not click two times the same baloon in order to gain more points
last_click_position = None

# Time to wait before the game starts
time.sleep(3)


# Function to compute the distance between the last baloon and the current detected baloon
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)



def find_and_click_template(template_path):
    global last_click_position

    # Taking a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)

    # Convert image to gray
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Reading the image(The baloon)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Search the template(the baloon)
    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

    # Get the prediction
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Compare the prediction to the threshold
    if max_val >= threshold:
        # Get the coordonates
        top_left = max_loc
        # Compute the center
        center_x = top_left[0] + template.shape[1] // 2
        center_y = top_left[1] + template.shape[0] // 2

        # Check if last click was the same baloon
        if last_click_position is None or calculate_distance((center_x, center_y), last_click_position) > double_click_threshold:
            # Move mouse to the coordonates
            mouse.Controller().position = (center_x, center_y)
            # Wait because moving the cursor takes time and might click before the cursor reaches the coordonates
            time.sleep(0.2)
            # Click
            mouse.Controller().click(mouse.Button.left)
            # Update last click
            last_click_position = (center_x, center_y)

            print("Clicked on the BALOON!")
        else:
            print("Baloon found, but double-click avoided.")
    else:
        print("Baloon not found.")


# If 'q' pressed, the program closes
while not keyboard.is_pressed('q'):
    find_and_click_template(template_path)
