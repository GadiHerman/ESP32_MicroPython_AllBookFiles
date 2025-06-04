import socket

CONTENT = b"""\
HTTP/1.0 200 OK


Hello from MicroPython!
"""

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 8080))
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    while True:
        res = s.accept()
        client_socket = res[0]
        req = client_socket.recv(4096)
        print("\n\n",req)
        client_socket.send(CONTENT)
        client_socket.close()

main()