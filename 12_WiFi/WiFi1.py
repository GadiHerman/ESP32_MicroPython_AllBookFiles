print("Scanning for WiFi networks, please wait...")
print("")


import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)


authmodes = ['Open', 'WEP', 'WPA-PSK' 'WPA2-PSK4', 'WPA/WPA2-PSK']
for (ssid, bssid, channel, RSSI, authmode, hidden) in sta_if.scan():
  print("* {:s}".format(ssid))
  print("   - Auth: {} {}".format(authmodes[authmode], '(hidden)' if hidden else ''))
  print("   - Channel: {}".format(channel))
  print("   - RSSI: {}".format(RSSI))
  print("   - BSSID: {:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(*bssid))
  print()
