from machine import Pin
from neopixel import NeoPixel
from time import sleep

np = NeoPixel(Pin(14), 8)

np[0] = (0, 255, 255)
np[1] = (255, 0, 255)
np[2] = (255, 255, 0)
np[3] = (0, 0, 255)
np[4] = (255, 0, 0)
np[5] = (0, 255, 0)
np[6] = (128, 128, 20)
np[7] = (128, 0, 200)
np.write()

sleep(2)

for i in range(8):
    np[i] = (0, 0, 0)
np.write()
