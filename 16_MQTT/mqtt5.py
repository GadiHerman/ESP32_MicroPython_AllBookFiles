from machine import Pin, PWM, Timer
from umqtt.simple import MQTTClient
import ujson
import os
import sys

CHANNEL_TOKEN = 'token_________________ku'
CHANNEL_NAME = 'esp32'
RESOURCE_NAME1 = 'servo'
RESOURCE_NAME2 = 'led'
MQTT_SERVER = 'mqtt.beebotte.com'
MQTT_USER = 'token:' + CHANNEL_TOKEN
MQTT_TOPIC1 = CHANNEL_NAME + '/' + RESOURCE_NAME1
MQTT_TOPIC2 = CHANNEL_NAME + '/' + RESOURCE_NAME2

servo_pin = Pin(23, Pin.OUT)
led_pin = Pin(2, Pin.OUT)
pwm = PWM(servo_pin, freq=50)

PING_PERIOD = 120
myTimer = Timer(0)

def handleTimerInt(timer):
    try:
        client.ping()
        print('Ping')
    except Exception as e:
        print('Ping error: ',e)

def set_servo_angle(angle):
    try:
        duty = int((angle / 180) * 75 + 40)
        pwm.duty(duty)
        print(f"Servo move to {angle} Degree")
    except Exception as e:
        print(f"Servo error: {e}")

def mqtt_callback(topic, msg):
    try:
        topic = topic.decode('utf-8')
        print(f"{topic}: {msg}")
        
        json_data = ujson.loads(msg)
        dt = json_data.get("data")
        
        if dt is None:
            print("No Data")
            return
            
        if not isinstance(dt, bool):
            print("Bool error")
            return
            
        if topic == MQTT_TOPIC1:
            #set_servo_angle(90 if dt else 0)
            if dt:
                set_servo_angle(90)
            else:
                set_servo_angle(0)
                
        elif topic == MQTT_TOPIC2:
            if dt:
                led_pin.value(1)
                print("LED ON")
            else:
                led_pin.value(0)
                print("LED OFF")
            
    except Exception as e:
        print(f"Error: {e}")

random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_' + str(random_num), 'utf-8')

client = MQTTClient(
    mqtt_client_id, 
    MQTT_SERVER,
    user=MQTT_USER,
    password='',
    keepalive=PING_PERIOD * 2
)


try:      
    client.connect()
    myTimer.init(period=PING_PERIOD*1000, mode=Timer.PERIODIC, callback=handleTimerInt)
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()
   
client.set_callback(mqtt_callback)
client.subscribe(MQTT_TOPIC1)
client.subscribe(MQTT_TOPIC2)


while True:
    try:
        client.wait_msg()
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        pwm.deinit()
        sys.exit()

