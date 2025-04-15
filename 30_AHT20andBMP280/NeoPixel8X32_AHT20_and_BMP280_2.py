from machine import Pin, I2C , RTC
from time import localtime, sleep
import ahtx0
import BMP280
import network
import ntptime
import NeoPixelMatrix
import sys

def connect_wifi():
    from time import sleep_ms
    if not sta_if.isconnected():
        print("Connecting to Wi-Fi", end="")
        # Activate station/Wi-Fi client interface
        sta_if.active(True)
        # Connect
        sta_if.connect(WIFI_SSID, WIFI_PSWD)
        # Wait untill the connection is estalished
        while not sta_if.isconnected():
            print(".", end="")
            sleep_ms(100)
        print(" Connected")

def disconnect_wifi():
    if sta_if.active():
        sta_if.active(False)
    if not sta_if.isconnected():
        print("Disconnected")

pin = 14
width = 32
height = 8
color1 = [80, 0, 0]
color2 = [0, 80, 0]
color3 = [0, 0, 80]
color4 = [80, 80, 0]
color5 = [0, 80, 80]
mat = NeoPixelMatrix.Matrix(Pin(pin), width, height, color1)
mat.CharSpacing=0
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq = 400000)
bmp = BMP280.BMP280(i2c, addr=0x77)
bmp.use_case(BMP280.BMP280_CASE_INDOOR)
bmp.oversample(BMP280.BMP280_OS_ULTRAHIGH)
bmp.temp_os = BMP280.BMP280_TEMP_OS_8
bmp.press_os = BMP280.BMP280_PRES_OS_8
bmp.standby = BMP280.BMP280_STANDBY_250
bmp.iir = BMP280.BMP280_IIR_FILTER_2
bmp.power_mode = BMP280.BMP280_POWER_FORCED
sensor = ahtx0.AHT10(i2c)

# Network settings
WIFI_SSID = "Herman2.4G"
WIFI_PSWD = "gal12asd"
UTC_OFFSET = 2  # CEST is UTC+2:00

# Create a clock object
rtc = RTC()

# Create Station interface
sta_if = network.WLAN(network.STA_IF)
connect_wifi()

# Get UTC time from NTP server (pool.ntp.org) and store it
# to internal RTC
ntptime.settime()

# Display UTC (Coordinated Universal Time / Temps Universel Coordonné)
(year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
print(f"UTC Time: {year}-{month}-{day} {hrs}:{mins}:{secs}")

# Get epoch time in seconds (for timezone update)
sec = ntptime.time()

disconnect_wifi()

# Update your epoch time in seconds and store in to internal RTC
sec = int(sec + UTC_OFFSET * 60 * 60)
(year, month, day, hrs, mins, secs, wday, yday) = localtime(sec)
rtc.datetime((year, month, day, wday, hrs, mins, secs, 0))

print(f"Local RTC time: UTC+{UTC_OFFSET}:00")

while True:
    try:
        (year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
        
        txt1 = "{:02}:{:02}".format(hrs,mins)
        txt2 = "{}/{}".format(day,month)
        txt3 = "{:.1f}%".format(sensor.relative_humidity)
        txt4 = "{:.1f}C".format(bmp.temperature) 
        txt5 = "{:.1f}".format((bmp.pressure/100))
        
        print("Time: ",hrs,":", mins,":",secs, sep="")
        print("Date: ",day,"/", month,"/",year, sep="")
        print(txt3,txt4,txt5)
        
        mat.show_text(txt1, scroll=False , color=color1)
        sleep(3)
        mat.show_text(txt2, scroll=False , color=color2)
        sleep(3)
        mat.show_text(txt3, scroll=False , color=color3)
        sleep(3)
        mat.show_text(txt4, scroll=False , color=color4)
        sleep(3)
        mat.show_text(txt5, scroll=False , color=color5)
        sleep(3)
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mat.clear()
        sys.exit()




