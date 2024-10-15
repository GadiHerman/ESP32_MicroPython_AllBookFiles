import time
from machine import Pin
led=Pin(15,Pin.OUT)
 
for x in range(100):
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    time.sleep(0.1)


led.value(1)
time.sleep(3)
led.value(0)