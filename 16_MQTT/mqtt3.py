from machine import Pin, Timer
from umqtt.simple import MQTTClient
import ujson
import sys
import os


LED = Pin(2, Pin.OUT)
PING_PERIOD   = 120


CHANNEL_TOKEN = 'token_jraXXXXXXXXXXUku'
CHANNEL_NAME  = 'esp32'
RESOURCE_NAME = 'led'
MQTT_SERVER = 'mqtt.beebotte.com'
MQTT_USER = 'token:' + CHANNEL_TOKEN
MQTT_TOPIC = CHANNEL_NAME + '/' + RESOURCE_NAME


def handleTimerInt(timer):
    client.ping()
    print('ping')
   
def callback_func(topic, msg):
    print("topic:",topic," msg:", msg)
    json_data= ujson.loads(msg)
    dt= json_data["data"]
    print("*** " + str(dt) + " ***")
    if dt:
        LED.value(1)
    else:
        LED.value(0)


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
   
client.set_callback(callback_func)
client.subscribe(MQTT_TOPIC)


while True:
    try:
        client.wait_msg()
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()
