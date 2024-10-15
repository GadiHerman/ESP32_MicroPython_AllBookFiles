from machine import Pin, ADC
import time


adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_9BIT) #For range between 0-511
while True:
    val = adc.read()
    val = val * (3.3 / 511)
    print(round(val, 2), "V")
    time.sleep_ms(1000)