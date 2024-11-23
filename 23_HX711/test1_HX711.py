from machine import Pin
from time import sleep_us, sleep_ms

class HX711:
    def __init__(self, pd_sck, dout, gain=128):
        self.pd_sck = Pin(pd_sck, Pin.OUT)
        self.dout = Pin(dout, Pin.IN)
        self.gain = gain
        
    def is_ready(self):
        return self.dout.value() == 0
        
    def read(self):
        # נחכה שהנתונים יהיו מוכנים
        while not self.is_ready():
            pass
            
        # נקרא 24 ביטים של נתונים
        data = 0
        for _ in range(24):
            self.pd_sck.value(1)
            sleep_us(1)
            data = (data << 1) | self.dout.value()
            self.pd_sck.value(0)
            sleep_us(1)
            
        # נשלח פולסים נוספים בהתאם לרווח הרצוי
        print(self.gain == 128 and 1 or self.gain == 64 and 3 or 2)
        for _ in range(self.gain == 128 and 1 or self.gain == 64 and 3 or 2):
            self.pd_sck.value(1)
            sleep_us(1)
            self.pd_sck.value(0)
            sleep_us(1)
            
        # נטפל במספר בסימן
        if data & 0x800000:
            data = data - 0x1000000
            
        return data
        
    def read_average(self, times=3):
        sum = 0
        for _ in range(times):
            sum += self.read()
            sleep_ms(100)
        return sum / times
        
# דוגמת שימוש
hx = HX711(pd_sck=13, dout=12)
value = hx.read_average()
OFFSET = hx.read_average(times=10)
print("OFFSET=",OFFSET)
SCALE = 10583.76/100
print("SCALE=",SCALE)
while True:
    
    value = hx.read_average()
    print((OFFSET-value)/SCALE)
    sleep_ms(1000)

