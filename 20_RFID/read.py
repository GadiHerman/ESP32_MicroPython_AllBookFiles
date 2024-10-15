from mfrc522 import MFRC522
from machine import Pin, SPI, reset

spi = SPI(2,baudrate=100000, polarity=0, phase=0, sck=Pin(18, Pin.OUT), mosi=Pin(23, Pin.OUT), miso=Pin(19, Pin.IN))  
rdr = MFRC522(spi, cs=Pin(5, Pin.OUT), rst=Pin(22, Pin.OUT))
print("Place the card close to the sensor")
print('Presse Ctrl-C to exit')

try:
    while True:
        stat, tag_type = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            stat, idCard = rdr.anticoll()
            if stat == rdr.OK:
                print("Card detected")
                cardId=[idCard[0], idCard[1], idCard[2], idCard[3]]
                print("  - id :", cardId)
            if rdr.select_tag(idCard) == rdr.OK:
                key = [255, 255, 255, 255, 255, 255]   
                if rdr.authentication(rdr.AUTHENT1A, 10, key, idCard) == rdr.OK:
                    print("Read data from card: %s" % rdr.read(10))
                    rdr.stop_crypto1()
                else:
                    print("Authentication error")
            else:
                print("Failed to select tag")
except KeyboardInterrupt:
    print('Ctrl-C pressed...exiting')
    reset()