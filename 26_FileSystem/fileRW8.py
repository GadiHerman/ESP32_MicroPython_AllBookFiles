count = 0
with open("myFile.txt", "a") as f:
    f.write("Now the file has more content!\n")
 
with open("myFile.txt", "r") as f:
    Lines = f.readlines()
    for line in Lines:
        count += 1
        print("Line",count,": ",  line.strip())