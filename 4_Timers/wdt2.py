from machine import WDT
import time

wdt = WDT(timeout=5000)

while True:
  
    print("Running...")
    wdt.feed()
    time.sleep(1)
    
    # סימולציית באג: לולאה אינסופית
    while True:
        pass 

