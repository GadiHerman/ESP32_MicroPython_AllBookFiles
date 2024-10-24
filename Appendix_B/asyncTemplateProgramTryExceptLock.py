import asyncio

async def myTask1(lock):
    while True:
        try:
            await lock.acquire()
            #
            #
            #
            print('I am myTask1 ')            
        except asyncio.CancelledError:
            print("Peripheral task canceled")
        except Exception as e:
            print("Error in ConnectionTask:", e)
        finally:
            await asyncio.sleep_ms(100)
            lock.release()
        
async def myTask2(lock):
    while True:
        try:
            await lock.acquire()
            #
            #
            #
            print('I am myTask2 ')            
        except asyncio.CancelledError:
            print("Peripheral task canceled")
        except Exception as e:
            print("Error in ConnectionTask:", e)
        finally:
            await asyncio.sleep_ms(1000)
            lock.release()
        
async def myTask3(lock):
    while True:
        try:
            await lock.acquire()
            #
            #
            #
            print('I am myTask3 ')            
        except asyncio.CancelledError:
            print("Peripheral task canceled")
        except Exception as e:
            print("Error in ConnectionTask:", e)
        finally:
            await asyncio.sleep_ms(500)
            lock.release()
            
#Run all tasks at the same time 
async def main():
    lock = asyncio.Lock()  # Main Lock instance
    t1 = asyncio.create_task(myTask1(lock))
    t2 = asyncio.create_task(myTask2(lock))
    t3 = asyncio.create_task(myTask3(lock))
    await asyncio.gather(t1, t2, t3)
    
#Running the main program
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped by user")

