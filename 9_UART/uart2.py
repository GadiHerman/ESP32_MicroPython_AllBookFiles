import uasyncio as asyncio
from machine import UART
uart = UART(2, 115200)


async def sender():
    i=0
    while True:
        s = 'Hello uart' + str(i) + '\n'
        uart.write(s)
        print(s)
        await asyncio.sleep(2)
        i=i+1


async def receiver():
    sreader = asyncio.StreamReader(uart)
    while True:
        res = await sreader.readline()
        print('Recieved', res)


loop = asyncio.get_event_loop()
loop.create_task(sender())
loop.create_task(receiver())
loop.run_forever()
