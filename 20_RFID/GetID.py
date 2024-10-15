from mfrc522 import MFRC522
from machine import Pin, SPI, reset

spi = SPI(2,baudrate=100000, polarity=0, phase=0, sck=Pin(18, Pin.OUT), mosi=Pin(23, Pin.OUT), miso=Pin(19, Pin.IN))  
rdr = MFRC522(spi, cs=Pin(5, Pin.OUT), rst=Pin(22, Pin.OUT))
print("Place the card close to the sensor")
print('Presse Ctrl-C to exit')

ApprovedCardList =  [
                        [58, 58, 199, 36],
                        [249, 65, 207, 153]
                    ]
try:
    while True:
        stat, tag_type = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            stat, raw_uid = rdr.anticoll()
            if stat == rdr.OK:
                cardId=[raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]]
                print("Card detected. id:",cardId)
                
                for lst in ApprovedCardList:
                    if lst == cardId:
                        print("OK")
                    
except KeyboardInterrupt:
    print('Ctrl-C pressed...exiting')
    reset()



