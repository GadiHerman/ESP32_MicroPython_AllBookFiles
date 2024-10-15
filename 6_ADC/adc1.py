from machine import Pin, ADC
adc_pin = Pin(34, mode=Pin.IN)
adc = ADC(adc_pin)
adc.atten(ADC.ATTN_11DB)
print(adc.read())
