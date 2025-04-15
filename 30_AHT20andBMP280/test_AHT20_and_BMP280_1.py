import utime
from machine import Pin, I2C
import ahtx0
from BMP280 import *

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq = 400000)

bmp = BMP280(i2c, addr=0x77)

bmp.use_case(BMP280_CASE_INDOOR)
bmp.oversample(BMP280_OS_ULTRAHIGH)

bmp.temp_os = BMP280_TEMP_OS_8
bmp.press_os = BMP280_PRES_OS_8

bmp.standby = BMP280_STANDBY_250
bmp.iir = BMP280_IIR_FILTER_2

bmp.power_mode = BMP280_POWER_FORCED



# Create the sensor object using I2C
sensor = ahtx0.AHT10(i2c)

while True:
    print("\nTemperature: %0.2f C" % sensor.temperature)
    print("Humidity: %0.2f %%" % sensor.relative_humidity)
    print("Temperature: %0.2f C" % bmp.temperature)
    print("Pressure: %0.2f %%" % (bmp.pressure/100))
    utime.sleep(5)