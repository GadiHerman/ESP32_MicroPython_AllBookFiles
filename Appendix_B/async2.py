import uasyncio as asyncio

# Create a lock
lock = asyncio.Lock()

async def myTadk1():
  # Acquire the lock
  await lock.acquire()
  try:
    # Access shared resource
    print("myTadk 1: acquired lock")
  finally:
    # Release the lock
    lock.release()

async def myTadk2():
  await lock.acquire()
  try:
    print("myTadk 2: acquired lock")
  finally:
    lock.release()

# Create an asyncio event loop
loop = asyncio.get_event_loop()
# Add tasks to the event loop
loop.create_task(myTadk1())
loop.create_task(myTadk2())
# Run the main loop
loop.run_forever()   
