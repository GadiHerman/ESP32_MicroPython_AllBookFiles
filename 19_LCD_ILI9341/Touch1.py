from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI, reset
WHITE = color565(255, 255, 255)

def touchscreen_press(x, y):
    y = (display.height - 1) - y
    display.draw_text8x8(60, 50, "X=%3d , Y=%3d" %(x, y), WHITE)
    print("X="+str(x)+" Y="+str(y))

spi1 = SPI(1, baudrate=4000000, sck=Pin(14), mosi=Pin(13))
display = Display(spi1, dc=Pin(4), cs=Pin(15), rst=Pin(27))
spi2 = SPI(2, baudrate=500000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
touch = Touch(spi2, cs=Pin(5), int_pin=Pin(2), int_handler=touchscreen_press)

display.clear()
display.draw_text8x8(50, 70, "Touch the screen!", WHITE)

try:
    while True:
        idle()
except KeyboardInterrupt:
    print("\nCtrl-C pressed. Cleaning up and exiting...")
finally:
    display.cleanup()
    reset()