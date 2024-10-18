from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI, reset

spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
display = Display(spi, dc=Pin(4), cs=Pin(15), rst=Pin(27))

display.draw_text8x8(0, 0, 'Hello from', color565(255, 0, 255))
display.draw_text8x8(16, 16, 'ESP32', color565(255, 255, 0))
display.draw_text8x8(32, 32, 'MicroPython', color565(0, 0, 255))

sleep(15)
display.cleanup()
reset()