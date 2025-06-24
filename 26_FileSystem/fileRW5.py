f = open("myFile.txt", "r")
for x in f:
  print(x.strip())
f.close()