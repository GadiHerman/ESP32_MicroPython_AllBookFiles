from machine import Pin
from neopixel import NeoPixel
from time import sleep

np = NeoPixel(Pin(14), 1)

np[0] = (0, 255, 255)
np.write()

sleep(1)

np[0] = (255, 0, 255)
np.write()

sleep(1)

np[0] = (255, 255, 0)
np.write()

sleep(1)

np[0] = (0, 0, 0)
np.write()