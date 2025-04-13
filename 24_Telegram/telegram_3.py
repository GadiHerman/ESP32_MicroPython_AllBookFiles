#file name telegram_3.py
import uasyncio as asyncio
from machine import Timer, UART, reset
import os
import sys
import json
import utelegram

uart = UART(2, 115200)

async def waiting():
    ch = ['-','\\','|','/']
    while True:
        for item in ch:
           print(item, end='\r')
           await asyncio.sleep(0.5)
        
async def receiver():
    print("Starts listening to serial communication")
    sreader = asyncio.StreamReader(uart)
    res =""
    while True:
        res = await sreader.readline()
        print('Recieved', res)

try:
    loop = asyncio.get_event_loop()
    loop.create_task(waiting())
    loop.create_task(receiver())
    loop.run_forever()

except KeyboardInterrupt:
    print('Ctrl-C pressed...exiting')
    client.disconnect()
    reset()

