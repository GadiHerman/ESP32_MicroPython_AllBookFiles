
from machine import TouchPad, Pin
import time

# Initialize the touch pin (GPIO 4)
touch_pin = TouchPad(Pin(4))

 # Adjust this threshold based on your touch sensor's sensitivity
TOUCH_THRESHOLD = 450

while True:
    touch_value = touch_pin.read()
    if touch_value < TOUCH_THRESHOLD:
        print("מגע מזוהה!")
    else:
        print("אין מגע")
    time.sleep(0.1)
