def long_process():
    print("Long Process Started")
    x = 0
    for i in range(10000):
        for j in range(100):
            x += i
    print(x)
    print("Long Process Completed")

def short_process():
    print("Short Process Started")
    for i in range(10):
        print(i, end=" ")
    print("\nShort Process Completed")

long_process()
short_process()
