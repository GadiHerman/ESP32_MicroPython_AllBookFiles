import time
from machine import Pin, time_pulse_us
from utime import sleep_us


def Get_distance_cm(trigger_pin=32,echo_pin=34):
       
    # Init trigger pin (out)
    trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
    # Init echo pin (in)
    echo = Pin(echo_pin, mode=Pin.IN, pull=None)


    # Send a 10us pulse.
    trigger.value(0)
    sleep_us(5)
    trigger.value(1)
    sleep_us(10)
    trigger.value(0)


    pulse_time = time_pulse_us(echo, 1, 500*2*30)
    cms = (pulse_time / 2) / 29.1   # 1cm each 29.1us
    return cms


for i in range(5):
    distance = Get_distance_cm()
    print('Distance:', distance, 'cm')
    time.sleep(2)
