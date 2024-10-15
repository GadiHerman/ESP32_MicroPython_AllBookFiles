import time
from micropython import const
from machine import Pin, Timer


BUTTON_A_PIN = const(26)
BUTTON_B_PIN = const(25)
BUTTON_C_PIN = const(33)
led1=Pin(13,Pin.OUT)
led2=Pin(12,Pin.OUT)
led3=Pin(14,Pin.OUT)
led4=Pin(27,Pin.OUT)


class Button:
    """
    Debounced pin handler
    usage e.g.:
    def button_callback(pin):
        print("Button (%s) changed to: %r" % (pin, pin.value()))
    button_handler = Button(pin=Pin(32, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_callback)
    """
    def __init__(self, pin, callback, trigger=Pin.IRQ_FALLING, min_ago=300):
        self.callback = callback
        self.min_ago = min_ago


        self._blocked = False
        self._next_call = time.ticks_ms() + self.min_ago


        pin.irq(trigger=trigger, handler=self.debounce_handler)


    def call_callback(self, pin):
        self.callback(pin)


    def debounce_handler(self, pin):
        if time.ticks_ms() > self._next_call:
            self._next_call = time.ticks_ms() + self.min_ago
            self.call_callback(pin)
        #else:
        #    print("debounce: %s" % (self._next_call - time.ticks_ms()))
       
       
def button_a_callback(pin):
    print("Button A (%s) changed to: %r" % (pin, pin.value()))
    led1.value(1)
    led2.value(1)
    led3.value(1)
    led4.value(1)


def button_b_callback(pin):
    print("Button B (%s) changed to: %r" % (pin, pin.value()))
    led1.value(0)
    led2.value(0)
    led3.value(0)
    led4.value(0)


def button_c_callback(pin):
    print("Button C (%s) changed to: %r" % (pin, pin.value()))




button_a = Button(pin=Pin(BUTTON_A_PIN, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_a_callback)
button_b = Button(pin=Pin(BUTTON_B_PIN, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_b_callback)
button_c = Button(pin=Pin(BUTTON_C_PIN, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_c_callback)
