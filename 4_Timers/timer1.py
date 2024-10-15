from machine import Pin, Timer


led1 = Pin(13,Pin.OUT)


def handleTimerInt(timer):
    led1.value(not led1.value())


myTimer = Timer(0)
myTimer.init(period=1000, mode=Timer.PERIODIC, callback=handleTimerInt)