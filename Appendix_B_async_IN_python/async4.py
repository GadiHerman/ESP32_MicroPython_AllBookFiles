RED = '\033[91m' # RED color codes
GREEN = '\033[92m' # GREEN color codes
BLUE = '\033[94m' # BLUE color codes
RESET = '\033[0m'  #Resets the color back to default

# Simple example
print(RED , "Text in RED color!" , RESET)
print(GREEN , "Text in GREEN color!" , RESET)
print(BLUE , "Text in BLUE color!" , RESET)

def print_red():
    for i in range(1, 101):
        print(RED , i , RESET, end="")

def print_green():
    for i in range(1, 101):
        print(GREEN , i , RESET, end="")

def main():
    print_red()
    print_green()

main()