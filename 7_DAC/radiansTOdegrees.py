import math

print("converts radians to degrees.")
radians = math.pi/2
degrees = radians * 180 / math.pi
print("radians",radians,"--> degrees",degrees)
print(math.sin(radians))

print("converts radians to degrees.")
print(math.degrees(0))
print(math.degrees(math.pi/2))
print(math.degrees(math.pi))
print(math.degrees(math.pi*1.5))

print("converts degrees to radians.")
print(math.sin(math.radians(0)))
print(math.sin(math.radians(90)))
print(math.sin(math.radians(180)))
print(math.sin(math.radians(270)))