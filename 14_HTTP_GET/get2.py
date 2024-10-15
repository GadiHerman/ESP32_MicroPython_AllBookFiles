import json
from machine import Pin


# load the config file from flash
f=open("data.json")
json_data = json.load(f)
print(json_data["is_led_on"])


# init LED
led = Pin(2, Pin.OUT)
led.value(json_data["is_led_on"])