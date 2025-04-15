from BMP280 import *
#from machine import SoftI2C, Pin
from machine import I2C, Pin

#i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq = 400000)

bmp = BMP280(i2c, addr=0x77)

bmp.use_case(BMP280_CASE_INDOOR)
bmp.oversample(BMP280_OS_ULTRAHIGH)

bmp.temp_os = BMP280_TEMP_OS_8
bmp.press_os = BMP280_PRES_OS_8

bmp.standby = BMP280_STANDBY_250
bmp.iir = BMP280_IIR_FILTER_2

# bmp.spi3w = BMP280_SPI3W_ON

# bmp.power_mode = BMP280_POWER_FORCED
# or 
bmp.force_measure()

# bmp.power_mode = BMP280_POWER_NORMAL
# or 
# bmp.normal_measure()
# also
#bmp.in_normal_mode()

# bmp.power_mode = BMP280_POWER_SLEEP
# or 
# bmp.sleep()

print(bmp.temperature)
print(bmp.pressure/100.0)

#True while measuring
bmp.is_measuring

#True while copying data to registers
bmp.is_updating