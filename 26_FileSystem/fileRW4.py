f = open("myFile.txt", "r")
count = 0
while True:
    count += 1
    line = f.readline()
    if not line:    # if line is empty
        break
    print("Line",count,": ",  line.strip())
f.close()
