import network
import ubinascii
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print (mac)
