import uasyncio as asyncio
from machine import UART
import _thread

bt_uart = UART(2, baudrate=9600)

async def bt_receiver():
    reader = asyncio.StreamReader(bt_uart)
    while True:
        try:
            line = await reader.readline()
            if line:
                print("[HC-05] >", line.decode().strip())
        except Exception as e:
            print("UART Read Error:", e)
            await asyncio.sleep(1)

def blocking_input_loop():
    print("Ready to send AT commands. Type and press Enter:")
    while True:
        try:
            line = input(">> ")
            bt_uart.write(line + "\r\n")
        except Exception as e:
            print("Input error:", e)

async def main():
    asyncio.create_task(bt_receiver())
    _thread.start_new_thread(blocking_input_loop, ())
    while True:
        await asyncio.sleep(1)

asyncio.run(main())
