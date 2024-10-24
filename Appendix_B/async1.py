import uasyncio as asyncio

async def myTadk():
    count = 0
    while True:
        count += 1
        print(count)
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.create_task(myTadk())
loop.run_forever()
