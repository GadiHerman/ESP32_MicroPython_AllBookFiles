import asyncio

RED = '\033[91m' # RED color codes
GREEN = '\033[92m' # GREEN color codes
BLUE = '\033[94m' # BLUE color codes
RESET = '\033[0m'  #Resets the color back to default

async def print_color(color=RED):
    for i in range(1, 101):
        print(color , i , RESET, end="")
        await asyncio.sleep(0)
        
async def main():
    await asyncio.gather(print_color(RED), print_color(GREEN), print_color(BLUE) )

#await main()
asyncio.run(main())