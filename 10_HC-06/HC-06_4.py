from machine import UART
import asyncio
from random import randint

uart = UART(2, 9600)
uart.init(9600, bits=8, parity=None, stop=1)
print(uart)

async def myTask1(lock):
    while True:
        try:
            await lock.acquire()
            if uart.any():
                data = uart.readline()
                #print('received:',data)
                # Convert byte string to a string using the decode() method
                decoded_string = data.decode("utf-8")            
                print('Data: ', decoded_string , type(decoded_string))            

        except asyncio.CancelledError:
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in ConnectionTask:", e)
        finally:
            await asyncio.sleep_ms(15)
            lock.release()
        
async def myTask2(lock):
    while True:
        try:
            await lock.acquire()
            num = randint(0,100)
            Data = str(num)+"\n"
            # Convert string to byte string using the encode() method
            sendData = Data.encode('utf-8')
            uart.write(sendData)
            print('Sent response:',sendData)          
        except asyncio.CancelledError:
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in ConnectionTask:", e)
        finally:
            await asyncio.sleep_ms(1000)
            lock.release()
        
            
#Run all tasks at the same time 
async def main():
    lock = asyncio.Lock()  # Main Lock instance
    t1 = asyncio.create_task(myTask1(lock))
    t2 = asyncio.create_task(myTask2(lock))
    await asyncio.gather(t1, t2)
    
#Running the main program
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped by user")


