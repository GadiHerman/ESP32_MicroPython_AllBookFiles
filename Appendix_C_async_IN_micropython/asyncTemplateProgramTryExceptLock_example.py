import uasyncio as asyncio
from machine import ADC, Pin
import time

temp_sensor = ADC(Pin(34))
light_sensor = ADC(Pin(35))

async def write_to_file(lock, filename, data):
    await lock.acquire()
    try:
        with open(filename, 'a') as f:
            f.write(data + '\n')
    finally:
        lock.release()

async def sample_temperature(lock):
    while True:
        value = temp_sensor.read()
        timestamp = time.time()
        data = f"{timestamp}, temp, {value}"
        print(data)
        await write_to_file(lock, 'sensor_data.txt', data)
        await asyncio.sleep(2)

async def sample_light(lock):
    while True:
        value = light_sensor.read()
        timestamp = time.time()
        data = f"{timestamp}, light, {value}"
        print(data)
        await write_to_file(lock, 'sensor_data.txt', data)
        await asyncio.sleep(5)

async def main():
    lock = asyncio.Lock()
    t1 = asyncio.create_task(sample_temperature(lock))
    t2 = asyncio.create_task(sample_light(lock))
    await asyncio.gather(t1, t2)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped by user")
