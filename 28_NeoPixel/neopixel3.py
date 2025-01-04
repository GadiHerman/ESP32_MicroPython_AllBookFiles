from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

np = NeoPixel(Pin(14), 8)
n = np.n

for i in range(100):
    for j in range(n):
        np[j] = (0, 0, 0)
    np[i % n] = (255, 255, 255)
    np.write()
    sleep_ms(25)

for i in range(8):
    np[i] = (0, 0, 0)
np.write()