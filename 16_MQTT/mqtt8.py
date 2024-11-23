# File name: mqtt8.py 
from machine import Timer
from umqtt.simple import MQTTClient
import utime
import os
import sys
import json

PUBLISH_PERIOD   = 5
timeSave = 0

CHANNEL_TOKEN = 'token_jr________________ku'
CHANNEL_NAME  = 'esp32'
RESOURCE_NAME = 'getdata'
MQTT_SERVER = 'mqtt.beebotte.com'
MQTT_USER = 'token:' + CHANNEL_TOKEN
MQTT_TOPIC = CHANNEL_NAME + '/' + RESOURCE_NAME

def handleTimerInt(timer):
    global timeSave
    thisdict = {
      "data": "Hello Gadi",
      "write": True
    }
    msg= json.dumps(thisdict, separators=(',', ':'))
    client.publish(MQTT_TOPIC,msg, qos=0)
    print("Publish:",msg, "MQTT_TOPIC=",MQTT_TOPIC)
    timeSave = 0
   
# create a random MQTT clientID
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')
client = MQTTClient(mqtt_client_id, MQTT_SERVER, user=MQTT_USER, password='', keepalive=PUBLISH_PERIOD*2  )
myTimer = Timer(0)

try:      
    client.connect()
    myTimer.init(period=PUBLISH_PERIOD*1000, mode=Timer.PERIODIC, callback=handleTimerInt)
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

while True:
    try:
        print('Publish new data in', (PUBLISH_PERIOD-timeSave) , "second. ", end="\r")
        utime.sleep(1)
        timeSave+=1
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()
