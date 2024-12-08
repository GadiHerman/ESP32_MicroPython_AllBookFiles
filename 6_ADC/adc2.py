from machine import Pin, ADC

adc = ADC(Pin(34)) # Create an ADC object linked to pin 34
adc.atten(ADC.ATTN_11DB)
print(adc.read())
