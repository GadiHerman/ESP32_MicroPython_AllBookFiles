from machine import Pin, DAC
import math

dac1 = DAC(Pin(25, Pin.OUT))
dac1.write(0)
dac2 = DAC(Pin(26, Pin.OUT))
dac2.write(0)

# global variables
P = 2
Q = 2
N = 200
A = 100
Omega = 2*math.pi/N

sin_table = []
cos_table = []
for i in range(N):
    arg = Omega*i
    x = A*math.sin(P*arg) + 127
    y = A*math.cos(Q*arg) + 127
    sin_table.append(int(x))
    cos_table.append(int(y))

index = 0 # index range: 0..(N-1)
while True:
    x = sin_table[index]
    y = cos_table[index]
    index = (index+1) % N
    dac1.write(x)
    dac2.write(y)
