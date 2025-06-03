import socket
from machine import ADC, Pin

SENSOR_ADC_PIN = 34
sensor_pin = Pin(SENSOR_ADC_PIN)
adc = ADC(sensor_pin)
adc.atten(ADC.ATTN_11DB)

def read_temperature():
    raw_value = adc.read()
    voltage = (raw_value / 4095) * 3.3
    temperature_celsius = voltage * 100
    return temperature_celsius

def start_temperature_server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8080))
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    while True:
        client_socket, client_address = s.accept()
        print("Client address:", client_address)
        try:
            request = client_socket.recv(1024)
            print("Request:")
            print(request)

            current_temperature = read_temperature()
            
            html_page_temp = """<!DOCTYPE html>
            <html>
            <head>
                <title>Temperature sensor</title>
                <style>
                  body {{ 
                    display: flex; 
                    flex-direction: column; 
                    align-items: center; 
                    justify-content: center; 
                    min-height: 100vh;
                    margin: 0; 
                    font-family: Arial, sans-serif;
                  }}
                  .container {{ 
                    padding: 20px;
                    text-align: center; 
                    border: 1px solid #ccc;
                    border-radius: 5px;
                  }}
                  h1 {{ 
                    font-size: 1.8em;
                    margin-bottom: 0.8em; 
                    color: #333;
                  }}
                  p {{ 
                    font-size: 1.1em;
                    margin-bottom: 0.5em; 
                    color: #555;
                  }}
                  strong {{ 
                    color: #000;
                  }}
                </style>
            </head>
            <body>
            <div class="container">
                <h1>Temperature sensor</h1>
                <p>Current temperature: <strong>{:.2f} &deg;C</strong></p>
            </div>
            </body>
            </html>
            """.format(current_temperature)

            response = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n" + html_page_temp
            client_socket.sendall(response)

        except OSError as e:
            print("OSError:", e)
        finally:
            client_socket.close()
            print("Client socket close.\n")

start_temperature_server()