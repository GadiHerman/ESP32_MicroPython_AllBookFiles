from machine import Pin, Timer
from umqtt.simple import MQTTClient
import ujson
import sys
import os
from time import sleep


LED = Pin(2, Pin.OUT)
PING_PERIOD   = 120


PUBLISH_PERIOD   = 10
msgNumber = 12.24


CHANNEL_TOKEN = 'token_jXXXXXXXXXXXXXXXXXu'
CHANNEL_NAME  = 'esp32'
MQTT_SERVER = 'mqtt.beebotte.com'
MQTT_USER = 'token:' + CHANNEL_TOKEN


RESOURCE_NAME_PUBLISH = 'sensor'
RESOURCE_NAME_SUBSCRIBE = 'led'
MQTT_TOPIC_PUBLISH = CHANNEL_NAME + '/' + RESOURCE_NAME_PUBLISH
MQTT_TOPIC_SUBSCRIBE = CHANNEL_NAME + '/' + RESOURCE_NAME_SUBSCRIBE


def handleTimer0Int(timer):
    client.ping()
    print('ping')


def handleTimer1Int(timer):
    global msgNumber
    global timeSave
    msg = b'{"data": ' + str(msgNumber) + b', "write": true}'
    client.publish(MQTT_TOPIC_PUBLISH,msg, qos=0)
    print("Publish:",msg)
    msgNumber += 1.12
    timeSave = 0


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


timer0 = Timer(0) #subscribe
timer1 = Timer(1) #publish


try:      
    client.connect()
    timer0.init(period=PING_PERIOD*1000, mode=Timer.PERIODIC, callback=handleTimer0Int)
    timer1.init(period=PUBLISH_PERIOD*1000, mode=Timer.PERIODIC, callback=handleTimer1Int)
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()
   
client.set_callback(callback_func)
client.subscribe(MQTT_TOPIC_SUBSCRIBE)


while True:
    try:
        client.wait_msg()
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()
