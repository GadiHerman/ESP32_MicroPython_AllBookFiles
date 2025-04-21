from machine import TouchPad, Pin
import time

# Initialize the touch pin (GPIO 4)
# The touch pin is usually a capacitive touch sensor pin
touch_pin = TouchPad(Pin(4))

while True:
    touch_value = touch_pin.read()
    print("touch_value:", touch_value)
    time.sleep(0.5)
