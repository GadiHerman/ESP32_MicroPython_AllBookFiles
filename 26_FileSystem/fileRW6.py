f = open("myFile.txt", "r")
count = 0
Lines = f.readlines()
for line in Lines:
    count += 1
    print("Line",count,": ",  line.strip())
f.close()
