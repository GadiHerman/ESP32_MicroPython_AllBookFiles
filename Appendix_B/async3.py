import uasyncio as asyncio

async def task(i, lock):
    while 1:
        await lock.acquire()
        print("Acquired lock in task", i)
        await asyncio.sleep(0.5)
        lock.release()

async def killer():
    await asyncio.sleep(10)

loop = asyncio.get_event_loop()

lock = asyncio.Lock()  # Global Lock instance
loop.create_task(task(1, lock))
loop.create_task(task(2, lock))
loop.create_task(task(3, lock))

loop.run_until_complete(killer())  # Run for 10s

