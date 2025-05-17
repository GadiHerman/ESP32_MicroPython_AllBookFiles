import time
from machine import UART

uart = UART(2, 115200)

def sender(i):
    s = 'Hello uart' + str(i) + '\n'
    uart.write(s)
    print(s)

def receiver():
    if uart.any():
        res = uart.readline()
        if res:
            print('Received', res)

i = 0
while True:
    sender(i)
    receiver()
    i += 1
    time.sleep(5)
