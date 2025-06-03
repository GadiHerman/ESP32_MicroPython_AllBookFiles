import socket
def html_page():
    html =  """
            <!DOCTYPE html>
            <html>
                <head>
                    <meta content="width=device-width, initial-scale=1">
                </head>
                <body>
                    <h1>Hello world!</h1>
                    <p>I am ESP32 in a web server mode</p>
                </body>
            </html>
            """
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8080))
s.listen(5)
print("Listening, connect your browser to http://<this_host>")
while True:
    client_socket, addr = s.accept()
    print("Got a connection from ",addr)
    request = client_socket.recv(1024)
    print("Content = ", request)
    response = html_page()
    client_socket.send("HTTP/1.1 200 OK")
    client_socket.send("Content-Type: text/html; encoding=utf8\nContent-Length: ")
    client_socket.send(str(len(response)))
    client_socket.send("\nConnection: close\n")
    client_socket.send("\n")
    client_socket.send(response)
    client_socket.close()

