from machine import Pin

def on_pressed(timer):
    print('pressed')

# Setup the button input pin with a pull-up resistor.
button = Pin(33, Pin.IN, Pin.PULL_UP)

# Register an interrupt on rising button input.
button.irq(on_pressed, Pin.IRQ_RISING)
