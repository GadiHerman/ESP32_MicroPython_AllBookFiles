import network
import socket
from machine import Pin
import time

# Define the LED pin (Built-in LED on GPIO 2 for most ESP32 boards)
led = Pin(2, Pin.OUT)
led.value(0)  # Initially turn OFF the LED

# WiFi Network Configuration
WIFI_SSID = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# WiFi Network Configuration
WIFI_SSID = "Herman2.4G"
WIFI_PASSWORD = "gal12asd"

# Connect to Local WiFi Network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

print("Connecting to WiFi network...")
while not wlan.isconnected():
    time.sleep(0.5)
    print("Waiting for connection...")

print("Connected to WiFi successfully!")
print("ESP32 IP Address:", wlan.ifconfig()[0])

# Initialize HTTP Web Server Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 80))
server_socket.listen(5)

print("HTTP API Server running on port 80. Awaiting requests...")

while True:
    client_socket, client_address = server_socket.accept()
    print("Incoming request from:", client_address)

    request = client_socket.recv(1024).decode('utf-8')
    
    # Process API endpoints
    if "GET /led/on" in request:
        led.value(1)
        print("Command received: Turning LED ON")
        response_body = "LED status: ON"
    elif "GET /led/off" in request:
        led.value(0)
        print("Command received: Turning LED OFF")
        response_body = "LED status: OFF"
    else:
        response_body = "ESP32 API Server Ready"

    # Send standard HTTP response header and body
    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n\r\n" + response_body
    )

    client_socket.sendall(http_response.encode('utf-8'))
    client_socket.close()

