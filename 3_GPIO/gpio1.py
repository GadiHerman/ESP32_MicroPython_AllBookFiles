from machine import Pin

pin_button = Pin(26, mode=Pin.IN, pull=Pin.PULL_UP)
pin_led = Pin(13, mode=Pin.OUT)
pin_led.on()

while True:
    if pin_button.value() == 1:
        pin_led.on()
    else:
        pin_led.off()
