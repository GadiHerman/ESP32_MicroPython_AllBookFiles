import time
from umqtt.robust import MQTTClient
import os
import sys
from machine import Pin
Led = Pin(2, mode=Pin.OUT, value=0) # 0V on output


# the following function is the callback which is
# called when subscribed data is received
def cb(topic, msg):
    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))
    if msg==b'OFF':
        Led.off()
    if msg==b'ON':
        Led.on()
       
# create a random MQTT clientID
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')




ADAFRUIT_IO_URL = b'io.adafruit.com'
ADAFRUIT_USERNAME = b'gadiHerman'
ADAFRUIT_IO_KEY = b'aio___XXX___0p3l'
ADAFRUIT_IO_SUB_FEEDNAME = b'led'
ADAFRUIT_IO_PUB_FEEDNAME = b'temperature'


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




# format of feed name: "ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME"
mqtt_pub_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_PUB_FEEDNAME), 'utf-8')
mqtt_sub_feedname = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_SUB_FEEDNAME), 'utf-8')
client.set_callback(cb)      
client.subscribe(mqtt_sub_feedname)
PUBLISH_PERIOD_IN_SEC = 10
SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5
accum_time = 0
temp=20
while True:
    try:
        # Publish
        if accum_time >= PUBLISH_PERIOD_IN_SEC:
            print('Publish:  temperature = {}'.format(temp))
            client.publish(mqtt_pub_feedname,    
                           bytes(str(temp), 'utf-8'),
                           qos=0)
            accum_time = 0                
            if temp<40:
                temp+=1
            else:
                temp=20        
        # Subscribe.  Non-blocking check for a new message.  
        client.check_msg()


        time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
        accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()
