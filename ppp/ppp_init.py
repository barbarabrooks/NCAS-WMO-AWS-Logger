import socket
import time

ip = '10.56.104.230' # IP of MOXA Nport - make a command line argument
port = int(4002) # pressure on port 2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #set up the socket

# try to connect
s.connect((ip, port)) # establish the connection
print('Connected to: ', ip, port)

msg1 = '\r' #shut up if talking 
msg2 = '.BP\r' #oout put continuously

s.sendall(msg1.encode())
s.sendall(msg4.encode())
