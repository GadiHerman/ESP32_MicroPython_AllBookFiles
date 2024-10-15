from machine import I2C, Pin
from i2c_lcd import I2C_LCD
from time import sleep_ms


i2c = I2C(scl=Pin(22), sda=Pin(21))
LCD = I2C_LCD(i2c,0x27)


LCD.print("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
sleep_ms(4000)
LCD.clear()
LCD.puts("Hello Word (-:  ")
n = 0
while 1:
    LCD.puts(n, 0, 1)
    n += 1
    sleep_ms(1000)