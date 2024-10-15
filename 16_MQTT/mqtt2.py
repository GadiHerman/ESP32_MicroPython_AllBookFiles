from machine import Pin
from umqtt.simple import MQTTClient
import ujson
import utime


LED = Pin(2, Pin.OUT)


def callback_func(topic, msg):
    print((topic, msg))
    json_data= ujson.loads(msg)
    dt= json_data["data"]
    if str(dt) == 'True':
        LED.value(1)
    if str(dt) == 'False':
        LED.value(0)


client = MQTTClient("test_mqtt_client_id", 'mqtt.beebotte.com', user='token:token_jraXXXXXXXXXXUku', password='', keepalive=30)
client.connect()
client.set_callback(callback_func)
client.subscribe('esp32/led')


while True:
    print("Checking msg...")
    client.check_msg()
    utime.sleep(1)
