import asyncio

RED = '\033[91m' # RED color codes
GREEN = '\033[92m' # GREEN color codes
BLUE = '\033[94m' # BLUE color codes
RESET = '\033[0m'  #Resets the color back to default

# Simple example
print(RED , "Text in RED color!" , RESET)
print(GREEN , "Text in GREEN color!" , RESET)
print(BLUE , "Text in BLUE color!" , RESET)

async def print_red():
    for i in range(1, 101):
        print(RED , i , RESET, end="")
        await asyncio.sleep(0)

async def print_green():
    for i in range(1, 101):
        print(GREEN , i , RESET, end="")
        await asyncio.sleep(0)

async def main():
    await asyncio.gather(print_green(), print_red())
#     task1 = asyncio.create_task(print_red())
#     task2 = asyncio.create_task(print_green())
#     await task1
#     await task2

#await main()
asyncio.run(main())