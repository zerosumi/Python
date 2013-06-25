'''
Created on Oct 4, 2012

@author: ElliottRen
'''
#import socket module
import sys
from socket import *





if len(sys.argv) < 2:
    serveraddr='127.0.0.1'
else:
    serveraddr=sys.argv[1]
if len(sys.argv) < 3:
    serverport=9000
else:
    serverport=int(sys.argv[2])
if len(sys.argv) < 4:
    serverpath='/'
else:
    serverpath=sys.argv[3]

clientSocket = socket(AF_INET,SOCK_STREAM)

print 'Connecting to server :', serveraddr,':', serverport

clientSocket.connect((serveraddr,serverport))

message = 'GET '+serverpath+' HTTP/1.1\r\nHost: '+serveraddr+':'+str(serverport)+'\r\n'
clientSocket.send(message)

data = clientSocket.recv(1024)
print repr(data)

clientSocket.close()