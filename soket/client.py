from socket import *

host = "localhost"
port = 8096
buf = 1024
addr = (host,port)

sock = socket(AF_INET,SOCK_DGRAM)
def_msg = "===Enter message to send to server===";
print ("\n",def_msg)

while (1):
    data = '>> '
    if not data:
        break
    else:
        if(sock.sendto(data,addr)):
            print ("Sending message '",data,"'.....")

sock.close()