import time
from umqtt.robust import MQTTClient
import os
import sys
from machine import Pin
Led = Pin(2, mode=Pin.OUT, value=0)


# the following function is the callback which is
# called when subscribed data is received
def cb(topic, msg):
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    if int(msg) < 30:
        Led.off()
    else:
        Led.on()


# create a random MQTT clientID
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')


# connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
ADAFRUIT_IO_URL = b'io.adafruit.com'
ADAFRUIT_USERNAME = b'gadiHerman'
ADAFRUIT_IO_KEY = b'aio_UKmN85Dbcr1QpriPBAmRTgbm0p3l'
ADAFRUIT_IO_FEEDNAME = b'temperature'


client = MQTTClient(client_id=mqtt_client_id,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
   
try:      
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()


mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')    
client.set_callback(cb)                    
client.subscribe(mqtt_feedname)  


# wait until data has been Published to the Adafruit IO feed
while True:
    try:
        client.wait_msg()
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()
