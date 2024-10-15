# This file is executed on every boot (including wake-boot from deepsleep)
import network
 
def connect():
  ssid = "yourNetworkName"
  password =  "yourNetworkPassword"
 
  station = network.WLAN(network.STA_IF)
 
  if station.isconnected() == True:
    print("Already connected")
    print(station.ifconfig())
    return
 
  station.active(True)
  station.connect(ssid, password)
 
  while station.isconnected() == False:
    pass
 
  print("Connection successful")
  print(station.ifconfig())

connect()
