from machine import UART
import time

bt_uart = UART(2, baudrate=38400)
#bt_uart = UART(2, baudrate=9600)

print("Enter AT commands (type and press Enter):")

while True:
    cmd = input(">> ")
    bt_uart.write(cmd + "\r\n")

    time.sleep(0.2)

    while bt_uart.any():
        response = bt_uart.readline()
        if response:
            print(response.decode().strip())
