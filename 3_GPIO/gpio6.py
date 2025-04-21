from machine import TouchPad, Pin
import time

touch_pin = TouchPad(Pin(4))

print("בצע כיול - אל תיגע בדק")
time.sleep(2)
samples = 10
sumsamples = 0
baseline = 0
for _ in range(samples):
    sumsamples += touch_pin.read()
baseline = (sumsamples / samples) 
THRESHOLD = baseline * 0.7  # 30% ירידה מערך הבסיס
print(f"ערך בסיס: {baseline}, סף: {THRESHOLD}")

while True:
    touch_value = touch_pin.read()
    if touch_value < THRESHOLD:
        print("מגע מזוהה!")
    time.sleep(0.1)

