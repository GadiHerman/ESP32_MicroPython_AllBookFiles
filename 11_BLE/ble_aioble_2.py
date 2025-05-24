import asyncio
import aioble
import bluetooth
from machine import Pin, ADC
import time

SERVICE_UUID = bluetooth.UUID('2b363f24-351f-4640-80ed-cb1f210228aa')
SEND_UUID = bluetooth.UUID('9ecdd7ad-48ad-40f2-af97-4872d2d90324')
RECEIV_UUID = bluetooth.UUID('f8d16e04-1304-4b43-8e4d-189bee24ab7a')

service = aioble.Service(SERVICE_UUID)
sendChara = aioble.Characteristic(service, SEND_UUID, read=True, notify=True)
receivChara = aioble.Characteristic(service, RECEIV_UUID, read=True, write=True, notify=True, capture=True)
aioble.register_services(service)


led = Pin(2, Pin.OUT)          # LED
temp_sensor = ADC(Pin(34))     # LM35
temp_sensor.atten(ADC.ATTN_11DB) 

def read_temperature():
    voltage = temp_sensor.read() * 3.3 / 4095 
    temp_c = voltage * 100  
    return temp_c

async def sendDataTask():
    while True:
        temperature = read_temperature()
        sendData = f"{temperature:.2f} C\n".encode('utf-8')
        sendChara.write(sendData, send_update=True)
        print('Send temperature:', sendData)
        await asyncio.sleep_ms(2000)

async def ConnectionTask():
    while True:
        try:
            con = await aioble.advertise(250_000, name="ESP32_BLE", services=[SERVICE_UUID])
            print("Connection from", con.device)
            await con.disconnected()
        except asyncio.CancelledError:
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in ConnectionTask:", e)
        finally:
            await asyncio.sleep_ms(200)

async def ReceivingTask():
    while True:
        try:
            connection, data = await receivChara.written()
            decoded = data.decode("utf-8").strip().upper()
            print("Received command:", decoded)
            if decoded == "ON":
                led.on()
                print("LED turned ON")
            elif decoded == "OFF":
                led.off()
                print("LED turned OFF")
            else:
                print("Unknown command")
        except asyncio.CancelledError:
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in ReceivingTask:", e)
        finally:
            await asyncio.sleep_ms(100)

async def main():
    t1 = asyncio.create_task(ConnectionTask())
    t2 = asyncio.create_task(sendDataTask())
    t3 = asyncio.create_task(ReceivingTask())
    await asyncio.gather(t1, t2, t3)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped by user")

