from machine import Pin
from neopixel import NeoPixel

np = NeoPixel(Pin(14), 1)
while True :
    np[0] = (0, 255, 255)
    np.write()