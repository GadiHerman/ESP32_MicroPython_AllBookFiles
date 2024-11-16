import time
from machine import Pin, PWM, Timer
from umqtt.simple import MQTTClient
import ujson
import os
import sys

# MQTT הגדרות
CHANNEL_TOKEN = 'token_jraXXXXXXXXXUku'
CHANNEL_NAME = 'esp32'
RESOURCE_NAME1 = 'servo'
RESOURCE_NAME2 = 'led'
MQTT_SERVER = 'mqtt.beebotte.com'
MQTT_USER = 'token:' + CHANNEL_TOKEN
MQTT_TOPIC1 = CHANNEL_NAME + '/' + RESOURCE_NAME1
MQTT_TOPIC2 = CHANNEL_NAME + '/' + RESOURCE_NAME2

# LED-הגדרת פינים עבור סרבו ו
servo_pin = Pin(23, Pin.OUT)
led_pin = Pin(2, Pin.OUT)
pwm = PWM(servo_pin, freq=50)

# MQTT הגדרת טיימר לשליחת פינג לשרת
PING_PERIOD = 120  # שניות
myTimer = Timer(0)

def handleTimerInt(timer):
    """MQTT שמירה על חיבור פעיל באמצעות פינג תקופתי"""
    try:
        client.ping()
        print('נשלח פינג')
    except Exception as e:
        print(f'שגיאת פינג: {e}')

def set_servo_angle(angle):
    """הגדרת זווית הסרבו בין 0 ל-180 מעלות"""
    try:
        # המרת זווית לערך מחזור עבודה (40-115 עבור סרבו SG90 טיפוסי)
        duty = int((angle / 180) * 75 + 40)
        pwm.duty(duty)
        print(f"הסרבו זז ל-{angle} מעלות")
    except Exception as e:
        print(f"שגיאת סרבו: {e}")

def mqtt_callback(topic, msg):
    """LED-טיפול בהודעות נכנסות עבור הסרבו וה"""
    try:
        topic = topic.decode('utf-8')
        print(f"התקבלה הודעה בנושא {topic}: {msg}")
        
        json_data = ujson.loads(msg)
        dt = json_data.get("data")
        
        if dt is None:
            print("בהודעה 'data' אין שדה")
            return
            
        if not isinstance(dt, bool):
            print("שהתקבל אינו ערך בוליאני 'data' שדה")
            return
            
        if topic == MQTT_TOPIC1:  # בקרת סרבו
            set_servo_angle(90 if dt else 0)
        elif topic == MQTT_TOPIC2:  # LED בקרת
            led_pin.value(1 if dt else 0)
            print(f"LED {'דולק' if dt else 'כבוי'}")
            
    except Exception as e:
        print(f"שגיאה בעיבוד ההודעה: {e}")

# עם מזהה אקראי MQTT יצירת לקוח
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_' + str(random_num), 'utf-8')

# MQTT יצירת והגדרת לקוח
client = MQTTClient(
    mqtt_client_id, 
    MQTT_SERVER,
    user=MQTT_USER,
    password='',
    keepalive=PING_PERIOD * 2
)

# התחברות והרשמה לנושאים
try:
    client.connect()
    myTimer.init(period=PING_PERIOD * 1000, mode=Timer.PERIODIC, callback=handleTimerInt)
    
    # הגדרת פונקציית callback והרשמה לשני הנושאים
    client.set_callback(mqtt_callback)
    client.subscribe(MQTT_TOPIC1)
    client.subscribe(MQTT_TOPIC2)
    
    print("MQTT מחובר לברוקר")
    
    # לולאה ראשית
    while True:
        client.check_msg()  # בדיקת הודעות ללא חסימה
        time.sleep(0.1)  # השהייה קטנה למניעת לולאה צפופה
        
except Exception as e:
    print(f"MQTT שגיאת: {type(e)._name_} {e}")
    sys.exit(1)
        
finally:
    try:
        client.disconnect()
        pwm.deinit()
    except:
        pass