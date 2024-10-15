from machine import Pin, ADC
import time


adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)
while True:
    val = adc.read()
    val = val * (3.3 / 4095)
    print(round(val, 2), "V")
    time.sleep_ms(1000)
