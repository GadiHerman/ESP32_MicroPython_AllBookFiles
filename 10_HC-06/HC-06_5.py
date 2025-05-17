from machine import UART
import utime


uart = UART(2, 9600)
uart.init(9600, bits=8, parity=None, stop=1)
print(uart)


while True:
    if uart.any():
        while uart.any():
            buf = uart.read()
            print('received:',buf)
            utime.sleep_ms(15)


        utime.sleep_ms(10)
        try:
            uart.write("OK")
            print('sent response')
        except OSError:
            pass
