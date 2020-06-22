import socket
try:
    IP = "151.101.94.133"
    host = socket.gethostbyaddr("IP")
    print(host, IP)
except (socket.gaierror):
    print("cannot resolve hostname: ", IP)