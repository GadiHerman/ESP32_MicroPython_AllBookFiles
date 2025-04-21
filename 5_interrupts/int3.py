from machine import Pin, Timer

def on_pressed1(timer):
    print('PIN 26 pressed')

def on_pressed2(timer):
    print('PIN 25 pressed')

def on_pressed3(timer):
    print('PIN 33 pressed')

def debounce1(pin):
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=on_pressed1)

def debounce2(pin):
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=on_pressed2)

def debounce3(pin):
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=on_pressed3)

timer = Timer(0)

button1 = Pin(26, Pin.IN, Pin.PULL_UP)
button2 = Pin(25, Pin.IN, Pin.PULL_UP)
button3 = Pin(33, Pin.IN, Pin.PULL_UP)
button1.irq(debounce1, Pin.IRQ_RISING)
button2.irq(debounce2, Pin.IRQ_RISING)
button3.irq(debounce3, Pin.IRQ_RISING)
