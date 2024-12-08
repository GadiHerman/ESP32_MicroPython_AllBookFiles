from machine import Pin
import time

pin_led = Pin(13, mode=Pin.OUT)
pin_led.on()
time.sleep(0.5)
pin_led.off()
time.sleep(0.5)
for x in range(1,10,2):
    pin_led.value(1)
    time.sleep(0.5)
    pin_led.value(0)
    time.sleep(0.5)
    print(x)
