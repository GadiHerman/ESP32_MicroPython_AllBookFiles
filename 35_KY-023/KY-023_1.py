from machine import Pin, ADC
from time import sleep_ms

# Setup analog reading for X and Y axes
joy_x = ADC(Pin(34))
joy_x.atten(ADC.ATTN_11DB) # Allow reading up to 3.3V

joy_y = ADC(Pin(35))
joy_y.atten(ADC.ATTN_11DB) # Allow reading up to 3.3V

# Setup digital input for the button with an internal pull-up resistor
joy_btn = Pin(32, Pin.IN, Pin.PULL_UP)

while True:
    # Read the analog values (0 to 4095)
    x_val = joy_x.read()
    y_val = joy_y.read()
    
    # Read the button state (0 means pressed, 1 means released)
    btn_val = joy_btn.value()
    
    # Print the values to the console
    print("X:", x_val, " | Y:", y_val, " | Button:", btn_val)
    
    # Wait half a second before the next reading
    sleep_ms(500)

