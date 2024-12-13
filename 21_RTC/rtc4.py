import ntptime
from machine import RTC
import network
from time import sleep

rtc=RTC()
ssid='______XXX______'
password='_____XXX______'
station=network.WLAN(network.STA_IF)
station.active (True)
station.connect(ssid,password)
print("Connecting to wifi: ",end="")
while station.isconnected()==False:
    print('.',end="")
    sleep (0.5)
print ("Connected")
ntptime.host="pool.ntp.org"
ntptime.settime()
while True:
    datetime=rtc.datetime()
    year=str(datetime[0])
    month=str(datetime[1])
    daymonth=str(datetime[2])
    dayweek=str(datetime[3])
    hour=str(datetime[4]+2)
    minute=str(datetime[5])
    second=str(datetime[6])
    print ("date: "+daymonth+"/"+month+"/"+year)
    print ("time: "+hour+":"+minute+":"+second)
    sleep (0.5)

