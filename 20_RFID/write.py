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
            (stat, idCard) = rdr.anticoll()
            if stat == rdr.OK:
                print("Card detected")
                cardId=[idCard[0], idCard[1], idCard[2], idCard[3]]
                print("  - id :", cardId)
                if rdr.select_tag(idCard) == rdr.OK:
                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                    DataToSend = [ord('G'),ord('a'),ord('d'),ord('i'),77,77,2,3,4,5,6,7,8,9,10,255]
                    if rdr.authentication(rdr.AUTHENT1A, 10, key, idCard) == rdr.OK:
                        stat = rdr.write(10, DataToSend)
                        rdr.stop_crypto1()
                        if stat == rdr.OK:
                            print("Data written to card")
                        else:
                            print("Failed to write data to card")
                    else:
                        print("Authentication error")
                else:
                    print("Failed to select tag")
except KeyboardInterrupt:
    print('Ctrl-C pressed...exiting')
    reset()







