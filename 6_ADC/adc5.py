from machine import Pin, ADC
from time import sleep

#joystick setup----------------------------
sw = Pin(13,Pin.IN, pull= Pin.PULL_UP)
x_pin = Pin(12,Pin.IN)
y_pin = Pin(14,Pin.IN)

x = ADC(x_pin)
y = ADC(y_pin)

x.atten(ADC.ATTN_11DB)
y.atten(ADC.ATTN_11DB)
#joystick setup----------------------------

#leds setup--------------------------------
led1 = Pin(27,Pin.OUT)
led2 = Pin(26,Pin.OUT)
led3 = Pin(25,Pin.OUT)
led4 = Pin(33,Pin.OUT)
led5 = Pin(32,Pin.OUT)

led_arr = [led1,led2,led3,led4,led5]
active_led = [1,0,0,0,0]
#leds setup--------------------------------

one_location = int

while True :
    
    for i in range(len(led_arr)): #reset all leds
        led_arr[i].value(0)
        
    one_location = active_led.index(1) #finds the active led
    
    if x.read() <= 500: #checks if the joystick moved to the left
        active_led = active_led[1:] + active_led[:1]
    elif x.read() >= 2200: #checks if the joystick moved to the right
        active_led = active_led[4:] + active_led[:4]
        
    led_arr[one_location].value(1)
    sleep(0.2)

# def check_joystick(): #test function to see the joystick values
#     print("x= " ,x.read())
#     print("y= " ,y.read(), "\n")

