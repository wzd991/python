#!usr/bin/env python 
# -*- coding:UTF-8 -*-
import socket
import time
import sys
client = None
try:
	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client.connect(("222.249.238.19",52010))
	print('server connect ok.')

except Exception as e:
	print(e)
	sys.exit()

while 1:
	data = input('please input work:').encode()
	try:
		print(type(data))
		client.send(data)
	except Exception as e:
		print(e)
		client.close()
		sys.exit()