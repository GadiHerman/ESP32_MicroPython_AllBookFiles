import machine, neopixel
from time import sleep
from random import randint

np = neopixel.NeoPixel(machine.Pin(14), 8)

while True:
    for i in range (8):
        np[i] = (randint(0,255), randint(0,255), randint(0,255))
        np.write()
        sleep(0.01)
    for i in range (8):
        np[i] = (0, 0, 0)
        np.write()
    for i in range (7,-1,-1):
        np[i] = (randint(0,255), randint(0,255), randint(0,255))
        np.write()
        sleep(0.01)
    for i in range (8):
        np[i] = (0, 0, 0)
        np.write()