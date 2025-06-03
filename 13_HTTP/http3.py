from machine import Pin
import socket

led = Pin(2, Pin.OUT)

def web_page():
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
 
  html = """
<html>
    <head>
        <title>ESP32 HTTP Server</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            html{
                display:inline-block;
                margin: 0px auto;
                text-align:
                center;}
            h1{
                color: #0F3376;
                padding: 2vh;}
            p{
                font-size: 1.5rem;}
            button{
                display: inline-block;
                background-color: #3668b8;
                border: none;
                border-radius: 4px;
                color: white;
                padding: 20px 30px;
                font-size: 25px;
                }
        </style>
    </head>
    <body>
        <h1>ESP32 HTTP Server</h1>
        <p>GPIO state: """ + gpio_state + """</p>
        <p><a href="/?led=on"><button>LED ON</button></a></p>
        <p><a href="/?led=off"><button>LED OFF</button></a></p>
    </body>
</html>
  """
  return html

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 8080))
s.listen(5)
print("Listening, connect your browser to http://<this_host>:8080/")

while True:
  client_socket, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = client_socket.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  
  if '/?led=on' in request:
    print('LED ON')
    led.value(1)
  elif '/?led=off' in request:
    print('LED OFF')
    led.value(0)      

  response = web_page()
  client_socket.send('HTTP/1.1 200 OK\n')
  client_socket.send('Content-Type: text/html\n')
  client_socket.send('Connection: close\n\n')
  client_socket.sendall(response)
  client_socket.close()
