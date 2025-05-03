from machine import DAC, Pin, reset
import time

dac = DAC(Pin(25))

wave = [ 0 , 0.4818 , 0.8443 , 0.998 ,  0.9048 , 0.5878 , 0.1253 , -0.3681, -0.7705,
 -0.9823, -0.9511, -0.6845, -0.2487,  0.2487 , 0.6845 , 0.9511 , 0.9823 , 0.7705,
  0.3681, -0.1253, -0.5878, -0.9048, -0.998 , -0.8443 ,-0.4818]
  
delay_us = 1

try:
    while True:
        for value in wave:
            dac.write(int((value + 1) * 127.5))
            time.sleep_us(delay_us)
       
except KeyboardInterrupt:
    print('Ctrl-C pressed...exiting')
    reset()