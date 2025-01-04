from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

np = NeoPixel(Pin(14), 8)
n = np.n

for i in range(0, 4 * 256, 8):
    for j in range(n):
        if (i // 256) % 2 == 0:
            val = i & 0xff
        else:
            val = 255 - (i & 0xff)
        np[j] = (val, 0, 0)
    np.write()

for i in range(n):
    np[i] = (0, 0, 0)
np.write()
