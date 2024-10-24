import asyncio
from machine import Pin
import time

# הגדרת פינים לדוגמה
led1 = Pin(2, Pin.OUT)
led2 = Pin(4, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)

async def blink_led(led, interval):
    """הבהוב LED במרווחי זמן קבועים"""
    while True:
        led.value(not led.value())
        await asyncio.sleep_ms(interval)

async def check_button():
    """בדיקת לחיצה על כפתור"""
    while True:
        if not button.value():  # כפתור נלחץ
            print("Button pressed!")
            await asyncio.sleep_ms(200)  # למניעת ריטוט
        await asyncio.sleep_ms(50)

async def read_sensor():
    """הדמיה של קריאת חיישן"""
    while True:
        # הדמיית קריאת חיישן שלוקחת זמן
        print("Reading sensor...")
        await asyncio.sleep_ms(1000)
        print("Sensor value: ", time.ticks_ms() % 100)

async def main():
    # יצירת משימות שרצות במקביל
    task1 = asyncio.create_task(blink_led(led1, 500))  # הבהוב כל חצי שנייה
    task2 = asyncio.create_task(blink_led(led2, 1000)) # הבהוב כל שנייה
    task3 = asyncio.create_task(check_button())
    task4 = asyncio.create_task(read_sensor())
    
    # הרצת כל המשימות במקביל
    await asyncio.gather(task1, task2, task3, task4)

# הפעלת הלולאה האסינכרונית
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped by user")