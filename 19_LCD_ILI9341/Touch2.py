from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI, reset

# Colors
CYAN = color565(0, 255, 255)
PURPLE = color565(255, 0, 255)
WHITE = color565(255, 255, 255)
GREEN = color565(0, 255, 0)
RED = color565(255, 0, 0)

# Button dimensions
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20

# Initialize LED
led = Pin(22, Pin.OUT)  # Adjust the pin number as needed

def draw_buttons():
    # Draw ON button
    display.fill_rectangle(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT, GREEN)
    display.draw_text8x8(60 - 8, 35 - 4, "ON", WHITE)
    
    # Draw OFF button
    display.fill_rectangle(10 + BUTTON_WIDTH + BUTTON_SPACING, 10, BUTTON_WIDTH, BUTTON_HEIGHT, RED)
    display.draw_text8x8(60 + BUTTON_WIDTH + BUTTON_SPACING - 12, 35 - 4, "OFF", WHITE)

def touchscreen_press(x, y):
    y = (display.height - 1) - y
    display.draw_text8x8(display.width // 2 - 32,
                              display.height - 9,
                              "{0:03d}, {1:03d}".format(x, y),
                              CYAN)
    if x>=10 and x<=10 + BUTTON_WIDTH and y>=10 and y<= 10 + BUTTON_HEIGHT:
        led.on()
        display.draw_text8x8(10, 100, "LED ON ", color565(255, 255, 255))
    elif x> 10 + BUTTON_WIDTH and x< display.width - 10  and y>=10 and y<= 10 + BUTTON_HEIGHT:
        led.off()
        display.draw_text8x8(10, 100, "LED OFF ", color565(255, 255, 255))
        
spi1 = SPI(1, baudrate=4000000, sck=Pin(14), mosi=Pin(13))
display = Display(spi1, dc=Pin(4), cs=Pin(15), rst=Pin(27))

spi2 = SPI(2, baudrate=500000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
touch = Touch(spi2, cs=Pin(5), int_pin=Pin(2), int_handler=touchscreen_press)

# Clear the screen
display.clear()

# Draw initial buttons
draw_buttons()

# Display initial message
display.draw_text8x8(60, 70, "Touch a button", WHITE)

try:
    while True:
        idle()
except KeyboardInterrupt:
    print("\nCtrl-C pressed. Cleaning up and exiting...")
finally:
    display.cleanup()
    reset()