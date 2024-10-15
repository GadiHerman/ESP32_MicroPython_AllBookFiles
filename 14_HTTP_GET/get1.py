import socket
s = socket.socket()
ai = socket.getaddrinfo("google.com", 80)
print("Address infos:", ai)
addr = ai[0][-1]
print("Connect address:", addr)
s.connect(addr)
s.send(b"GET / HTTP/1.0\r\n\r\n")
print(s.recv(4096))
s.close()