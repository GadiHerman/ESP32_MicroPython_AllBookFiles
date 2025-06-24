import os

try:
    os.remove("demofile.txt")
except OSError:
    print("The file does not exist")