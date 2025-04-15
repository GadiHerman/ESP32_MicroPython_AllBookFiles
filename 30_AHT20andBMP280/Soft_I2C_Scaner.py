from machine import SoftI2C, Pin

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

devices = i2c.scan()
if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices))
for device in devices:
    print("At address: ",hex(device))