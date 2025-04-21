from machine import WDT
import time

wdt = WDT(timeout=5000)

while True:
    print("Running...")
    # Uncomment the next line to see the watchdog timer in action
    wdt.feed()  # Reset the watchdog timer
    time.sleep(1) # Simulate some work
    
