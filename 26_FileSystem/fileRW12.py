import os

# Check if the 'letters' directory exists, and create it if it doesn't
try:
    os.stat('letters')
except OSError:
    os.mkdir('letters')

# Open 'demofile.txt' in write mode and write lines to it
with open("letters/demofile.txt", "w") as f:
    f.write("This is the first line.\n")
    f.write("Second line here.\n")
    f.write("And the third.\n")
    f.write("Finally, the last line.\n")

# Open 'demofile.txt' in read mode and print each line
with open("letters/demofile.txt", "r") as f:
    lines = f.readlines()
    count = 0
    for line in lines:
        count += 1
        print("Line", count, ": ", line.strip())
