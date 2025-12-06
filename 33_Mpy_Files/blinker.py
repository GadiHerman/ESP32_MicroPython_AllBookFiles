from machine import Pin
import time

def blink_led(pin_num, times):
    led = Pin(pin_num, Pin.OUT)
    for i in range(times):
        led.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(0.5)
    print("Blinking finished.")
