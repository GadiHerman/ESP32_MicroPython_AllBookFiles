import network
import urequests
import ujson
import utime
from machine import RTC


ssid = "Herman2.4G"      #wifi name
pw = "gal12asd"           #wifi password
web_query_delay = 200000    #interval time of web JSON query
url = "http://www.worldtimeapi.org/api/timezone/Asia/Jerusalem.txt"


# wifi connection
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, pw)
while not wifi.isconnected():
    pass
print("IP Address:" , str(wifi.ifconfig()[0]))


#internal RTC(Real Time Clock)
rtc = RTC()     
update_time = utime.ticks_ms() - web_query_delay


while True:
    if not wifi.isconnected():
        machine.reset() # if lose wifi connection reboot ESP32
    if utime.ticks_ms() - update_time >= web_query_delay:
        response = urequests.get(url)
        if response.status_code == 200: # if query success
            #print("Date&Time in JSON format: " + response.text)
            js = ujson.loads(response.text) # you can also use parsed = response.json()
            s_dt = str(js["datetime"])
            year = int(s_dt[0:4])
            month = int(s_dt[5:7])
            day = int(s_dt[8:10])
            hour = int(s_dt[11:13])
            minute = int(s_dt[14:16])
            second = int(s_dt[17:19])
            subsecond = int(round(int(s_dt[20:26]) / 10000))
            # update internal RTC
            rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
            update_time = utime.ticks_ms()
            print("RTC updated\n")   
    dt = rtc.datetime()    
    s_date = "{:02}/{:02}/{:4}".format(dt[1], dt[2], dt[0])
    s_time = "{:02}:{:02}:{:02}".format(dt[4], dt[5], dt[6])
    print("Date: " + s_date)
    print("Time: " + s_time)
    utime.sleep(2)
