from hx711 import HX711
from machine import reset
import time

hx = HX711(12, 13)

hx.Calibrate()            #Calibrate the weight to zero

hx.set_scale(-105.4) #Converts data to weight in grams

try:
    while True:
        val = hx.get_units(10)
        print(val)
        time.sleep_ms(500)
                   
except KeyboardInterrupt:
    print('Ctrl-C pressed...exiting')
    reset()

