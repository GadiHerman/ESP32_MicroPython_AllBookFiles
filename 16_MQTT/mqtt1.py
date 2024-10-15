from umqtt.simple import MQTTClient
import ujson
import utime


def callback_func(topic, msg):
    print((topic, msg))


client = MQTTClient("test_mqtt_client_id", 'mqtt.beebotte.com', user='token:token_jraXXXXXXXXXXXUku', password='', keepalive=30)
client.connect()
client.set_callback(callback_func)
client.subscribe('esp32/led')


while True:
    print("Checking msg...")
    client.check_msg()
    utime.sleep(1)