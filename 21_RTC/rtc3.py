from machine import RTC, reset
import ntptime
from time import localtime, sleep

UTC_OFFSET = 3  # UTC+3:00

# Create an independent clock object
rtc = RTC()

print(rtc.datetime())

# Get UTC time from NTP server (pool.ntp.org) and store it to internal RTC
ntptime.settime()

# Display UTC (Coordinated Universal Time / Temps Universel Coordonné)
(year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
print(f"UTC Time: {year}-{month}-{day} {hrs}:{mins}:{secs}")

# Get epoch time in seconds (for timezone update)
sec = ntptime.time()

# Update your epoch time in seconds and store in to internal RTC
sec = int(sec + UTC_OFFSET * 60 * 60)
(year, month, day, hrs, mins, secs, wday, yday) = localtime(sec)
rtc.datetime((year, month, day, wday, hrs, mins, secs, 0))

print(f"Local RTC time: UTC+{UTC_OFFSET}:00")

try:
    while True:
        # Read values from internal RTC
        (year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
        print(f"{year}-{month}-{day} {hrs}:{mins}:{secs}")

        # Delay 30 seconds
        sleep(30)
        
except KeyboardInterrupt:
    print('Ctrl-C pressed...exiting')
    reset()