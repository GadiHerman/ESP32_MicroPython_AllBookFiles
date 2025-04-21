import asyncio
from concurrent.futures import ProcessPoolExecutor

def cpu_heavy_task():
    print("Long Process Started (in process)")
    x = 0
    for i in range(10000):
        for j in range(10000):
            x += i
    print(x)
    print("Long Process Completed (in process)")

async def short_process():
    print("Short Process Started")
    for i in range(10):
        print(i, end=" ")
        await asyncio.sleep(0.1)
    print("\nShort Process Completed")

async def main():
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        # מפעיל את הקוד הכבד בתהליך נפרד
        long_task = loop.run_in_executor(pool, cpu_heavy_task)
        short_task = short_process()
        await asyncio.gather(long_task, short_task)

# The main function is the entry point of the program for Python 3.7 and above.
# It is the recommended way to run asyncio programs.
# Run the main function in the event loop 
if __name__ == "__main__":
    asyncio.run(main())

# If you are using Jupyter Notebook or IPython, you can use the following code instead:
#await main()
