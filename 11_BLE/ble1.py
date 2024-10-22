import asyncio
import aioble
import bluetooth
from random import randint

#Personal UUID generator https://www.uuidgenerator.net
SERVICE_UUID = bluetooth.UUID('2b363f24-351f-4640-80ed-cb1f210228aa')
SEND_UUID = bluetooth.UUID('9ecdd7ad-48ad-40f2-af97-4872d2d90324')
RECEIV_UUID = bluetooth.UUID('f8d16e04-1304-4b43-8e4d-189bee24ab7a')

#Create service and characteristics
service = aioble.Service(SERVICE_UUID)
sendChara = aioble.Characteristic(service, SEND_UUID, read=True, notify=True)
receivChara = aioble.Characteristic(service, RECEIV_UUID, read=True, write=True, notify=True, capture=True)
aioble.register_services(service)

async def sendDataTask():
    while True:
        num = randint(0,100)
        sendData = str(num)+"\n"
        # Convert string to byte string using the encode() method
        sendData = sendData.encode('utf-8')
        sendChara.write(sendData, send_update=True)
        print('Send data: ', sendData)
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
            print('Data: ', data , type(data))            
            # Convert byte string to a string using the decode() method
            decoded_string = data.decode("utf-8")            
            print('Data: ', decoded_string , type(decoded_string))            
        except asyncio.CancelledError:
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in ReceivingTask:", e)
        finally:
            await asyncio.sleep_ms(100)
            
#Run all tasks at the same time 
async def main():
    t1 = asyncio.create_task(ConnectionTask())
    t2 = asyncio.create_task(sendDataTask())
    t3 = asyncio.create_task(ReceivingTask())
    await asyncio.gather(t1, t2, t3)
    
#Running the main program
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped by user")