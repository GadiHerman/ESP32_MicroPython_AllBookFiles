import asyncio

async def myTask1():
    while True:
        try:
            #
            #
            #
            print('I am myTask1 ')            
        except asyncio.CancelledError:
            print("Peripheral task canceled")
        except Exception as e:
            print("Error in ConnectionTask:", e)
        finally:
            await asyncio.sleep_ms(2000)
        
async def myTask2():
    while True:
        try:
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
        
async def myTask3():
    while True:
        try:
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
            
#Run all tasks at the same time 
async def main():
    t1 = asyncio.create_task(myTask1())
    t2 = asyncio.create_task(myTask2())
    t3 = asyncio.create_task(myTask3())
    await asyncio.gather(t1, t2, t3)
    
#Running the main program
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped by user")
