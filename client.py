from socket import *
import  sys
import os
serverName = '127.0.0.1'
serverPort = 3999

import  time
client = []
datacache = []
cnt = 0
while True:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    client.append(clientSocket)
    cnt+=1
    try:
        clientSocket.connect((serverName, serverPort))
        print(cnt)
        # client.append(clientSocket)
        # time.sleep(0.01)
    except Exception as e:
        print(e)
        sys.exit()
# try:
#     while True:
#         sentence = input('Input lowercase sentence:').encode()
#         print(type(sentence))
#         msg = bytearray(sentence)
#         clientSocket.send(msg)
#         modifiedSentence = clientSocket.recv(1024)
#         print('From Server:{}'.format(modifiedSentence))
# except Exception as e:
#     print(e)
#     clientSocket.close()
