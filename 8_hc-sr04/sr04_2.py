import time
from hcsr04 import HCSR04


sensor = HCSR04(trigger_pin=32, echo_pin=34)
for i in range(10):
    distance = sensor.distance_cm()
    print('Distance:', distance, 'cm')
    time.sleep(1.5)