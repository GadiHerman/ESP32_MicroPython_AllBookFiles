from machine import RTC

rtc = RTC()
print("Current time:" + str(rtc.datetime()))

(year, month, day, wday, hrs, mins, secs, subsecs) = rtc.datetime()
print("Time: ",hrs,":", mins,":",secs, sep="")
print("Date: ",day,"/", month,"/",year, sep="")