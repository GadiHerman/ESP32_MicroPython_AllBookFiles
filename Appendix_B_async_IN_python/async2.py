import asyncio

async def long_process():
    print("Long Process Started")
    x = 0
    for i in range(10000):
        for j in range(100):
            x += i
        if i % 100 == 0:
            # in end of every 100 iterations, we yield control to the Event Loop
            # to allow other tasks to run
            await asyncio.sleep(0)  
    print(x)
    print("Long Process Completed")

async def short_process():
    print("Short Process Started")
    for i in range(10):
        print(i, end=" ")
        await asyncio.sleep(0)  # משחרר שליטה ל-event loop
    print("\nShort Process Completed")

async def main():
    await asyncio.gather(long_process(), short_process())

# The main function is the entry point of the program for Python 3.7 and above.
# It is the recommended way to run asyncio programs.
# Run the main function in the event loop 
if __name__ == "__main__":
    asyncio.run(main())

# If you are using Jupyter Notebook or IPython, you can use the following code instead:
#await main()