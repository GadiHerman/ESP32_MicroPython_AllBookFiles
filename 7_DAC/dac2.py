from machine import Pin, DAC
import math


dac = DAC(Pin(25, Pin.OUT))
dac.write(0)


P = 2
N = 200
A = 100
Omega = 2*math.pi/N


sin_table = []
for i in range(N):
    arg = Omega*i
    x = A*math.sin(P*arg) + 127
    sin_table.append(int(x))


index = 0
while True:
    dac.write(sin_table[index])
    index = (index+1) % N