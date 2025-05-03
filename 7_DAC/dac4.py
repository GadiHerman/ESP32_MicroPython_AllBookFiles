from machine import DAC, Pin, reset
import time
import math

dac = DAC(Pin(25))

samples = 50
wave = []
for i in range(samples):
    angle = 2 * math.pi * i / samples
    wave.append(int((math.sin(angle) + 1) * 127.5)) 

delay_us = 1  # זמן השהיה בין דגימות במיקרו-שניות

try:
    while True:
        for value in wave:
            dac.write(value)
            time.sleep_us(delay_us)
       
except KeyboardInterrupt:
    print('Ctrl-C pressed...exiting')
    reset()




