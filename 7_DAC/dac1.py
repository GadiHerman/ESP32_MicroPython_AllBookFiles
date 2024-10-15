from machine import DAC, Pin
import time
dac = DAC(Pin(25))
for i in range(10):
    dac.write(0)
    print("0V")
    time.sleep_ms(3000)
    dac.write(128)
    print("1.65V")
    time.sleep_ms(3000)
    dac.write(255)
    print("3.3V")
    time.sleep_ms(3000)