from machine import Pin, Timer

interruptCounter = 0
led1 = Pin(13,Pin.OUT)

def handleTimerInt(timer):
    led1.value(not led1.value())
    global interruptCounter
    interruptCounter = interruptCounter+1
    print("Interrupt has occurred: " + str(interruptCounter))

myTimer = Timer(0)
myTimer.init(period=300, mode=Timer.PERIODIC, callback=handleTimerInt)