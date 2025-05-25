from machine import Pin
import socket

# הגדרת פיני LED
led1 = Pin(2, Pin.OUT)
led2 = Pin(4, Pin.OUT)
led3 = Pin(5, Pin.OUT)

# הגדרת פיני מפסקים
switch1 = Pin(12, Pin.IN, Pin.PULL_UP)
switch2 = Pin(14, Pin.IN, Pin.PULL_UP)

def web_page():
    # מצבי LED
    led1_state = "ON" if led1.value() else "OFF"
    led2_state = "ON" if led2.value() else "OFF"
    led3_state = "ON" if led3.value() else "OFF"

    # קריאת מצב מפסקים
    switch1_state = "PRESSED" if switch1.value() == 0 else "RELEASED"
    switch2_state = "PRESSED" if switch2.value() == 0 else "RELEASED"

    html = """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 Control Panel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        html {{ text-align: center; font-family: Arial; }}
        button {{
            background-color: #4CAF50; border: none; color: white;
            padding: 16px 40px; margin: 10px; font-size: 20px;
            border-radius: 8px; cursor: pointer;
        }}
        .off {{ background-color: #f44336; }}
    </style>
</head>
<body>
    <h1>ESP32 Web Control</h1>

    <p>LED1 is <strong>{led1}</strong></p>
    <a href="/?led1=on"><button>LED1 ON</button></a>
    <a href="/?led1=off"><button class="off">LED1 OFF</button></a>

    <p>LED2 is <strong>{led2}</strong></p>
    <a href="/?led2=on"><button>LED2 ON</button></a>
    <a href="/?led2=off"><button class="off">LED2 OFF</button></a>

    <p>LED3 is <strong>{led3}</strong></p>
    <a href="/?led3=on"><button>LED3 ON</button></a>
    <a href="/?led3=off"><button class="off">LED3 OFF</button></a>

    <h2>Switch Status</h2>
    <p>Switch 1: <strong>{sw1}</strong></p>
    <p>Switch 2: <strong>{sw2}</strong></p>
</body>
</html>""".format(led1=led1_state, led2=led2_state, led3=led3_state,
                  sw1=switch1_state, sw2=switch2_state)
    return html

# יצירת סוקט
s = socket.socket()
ai = socket.getaddrinfo("0.0.0.0", 8080)
addr = ai[0][-1]
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)

print("Listening on http://<ESP32_IP>:8080")

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)

    # בדיקת בקשות להפעלת נוריות
    if '/?led1=on' in request:
        led1.value(1)
    if '/?led1=off' in request:
        led1.value(0)
    if '/?led2=on' in request:
        led2.value(1)
    if '/?led2=off' in request:
        led2.value(0)
    if '/?led3=on' in request:
        led3.value(1)
    if '/?led3=off' in request:
        led3.value(0)

    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()


