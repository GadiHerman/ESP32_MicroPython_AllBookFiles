#file name mqtt9.py
import uasyncio as asyncio
from machine import UART
from machine import Timer, UART, reset
from umqtt.simple import MQTTClient
import os
import sys
import json

uart = UART(2, 115200)
PING_PERIOD = 120

CHANNEL_TOKEN = 'token_jr______________ku'
CHANNEL_NAME  = 'esp32'
RESOURCE_NAME = 'getdata'
MQTT_SERVER = 'mqtt.beebotte.com'
MQTT_USER = 'token:' + CHANNEL_TOKEN
MQTT_TOPIC = CHANNEL_NAME + '/' + RESOURCE_NAME

def handleTimerInt(timer):
    client.ping()
    print('Ping to MQTT server')

async def waiting():
    ch = ['-','\\','|','/']
    while True:
        for item in ch:
           print(item, end='\r')
           await asyncio.sleep(0.5)
        
async def receiver():
    print("Starts listening to serial communication")
    sreader = asyncio.StreamReader(uart)
    res =""
    while True:
        res = await sreader.readline()
        print('Recieved', res)
        myDict = {
          "data": res,
          "write": True
        }
        msg= json.dumps(myDict, separators=(',', ':'))
        client.publish(MQTT_TOPIC,msg, qos=0)
        print("Publish:",msg, "MQTT_TOPIC=",MQTT_TOPIC)
     
# create a random MQTT clientID
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')
client = MQTTClient(mqtt_client_id, MQTT_SERVER, user=MQTT_USER, password='', keepalive=PING_PERIOD*2  )
myTimer = Timer(0)

try:      
    client.connect()
    myTimer.init(period=PING_PERIOD*1000, mode=Timer.PERIODIC, callback=handleTimerInt)
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

print("Connect to MQTT server!")

try:
    loop = asyncio.get_event_loop()
    loop.create_task(waiting())
    loop.create_task(receiver())
    loop.run_forever()

except KeyboardInterrupt:
    print('Ctrl-C pressed...exiting')
    client.disconnect()
    reset()
