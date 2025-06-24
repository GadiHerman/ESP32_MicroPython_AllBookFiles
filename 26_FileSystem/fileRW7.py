count = 0
with open("myFile.txt", "r") as f:   #f = open("myFile.txt", "r")
    Lines = f.readlines()
    for line in Lines:
        count += 1
        print("Line",count,": ",  line.strip())
#f.close()
