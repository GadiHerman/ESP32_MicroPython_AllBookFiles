from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

np = NeoPixel(Pin(14), 8)
n = np.n

for i in range(100):
    for j in range(n):
        np[j] = (0, 0, 128)
    if (i // n) % 2 == 0:
        np[i % n] = (0, 0, 0)
    else:
        np[n - 1 - (i % n)] = (0, 0, 0)
    np.write()
    sleep_ms(60)

for i in range(8):
    np[i] = (0, 0, 0)
np.write()