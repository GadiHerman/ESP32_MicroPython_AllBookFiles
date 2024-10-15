from machine import Pin, I2C
import ssd1306
from time import sleep


# using default address 0x3C
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


oled.text('Hello, World!', 0, 0)
oled.text('Gadi', 0, 10)
oled.text('Herman', 0, 20)
       
oled.show()
