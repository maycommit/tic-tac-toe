# import socket
# import threading
from socket import *

host = "localhost"
port = 8096
buf = 1024
addr = (host,port)

sock = socket(AF_INET,SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind(addr)

print ("Websocket active.")
print ("address:\t"+host+":"+str(port))

while 1:
    data,addr = sock.recvfrom(buf)
    if not data:
        print ("Client has exited!")
        break
    else:
        print ("\nReceived message '", data,"'")

# Close socket
sock.close()