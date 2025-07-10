import os
import machine

sd = machine.SDCard(slot=2)
os.mount(sd, "/sd")

contents = os.listdir('/sd')
print("Directory contents:", contents)