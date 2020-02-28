#!usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import sys
import socketserver
import socket
import threading
'''
设备识别方式采用格式化序列号识别。
通过 type + sn 模式组成.
TERNAL = 0x01000000
DEV    = 0x02000000
ADMIN  = 0X30000000
处理机制采用事件处理方式。

client  ---- msg---> server -----> termal
termal  ---- msg---> server -----> client.
client  ---- log --> server (save)
'''
logging.basicConfig(format="%(asctime)s %(thread)d %(threadName)s %(message)s",stream=sys.stdout,level=logging.INFO)
clients = []

class sever_Handler(socketserver.BaseRequestHandler):
    def setup(self):
        super().setup()
        self.event = threading.Event()
        logging.info('setup:{}'.format(self.request))
        clients.append(self.request)

    def handle(self):
        super().handle()
        while not self.event.is_set():
            try:
                data = self.request.recv(1024).decode()
            except Exception as e:
                logging.info(e)
                break

            logging.info(data)
            msg = "{}-{}".format(self.client_address,data).encode()
            sk.send(msg)

    def finish(self):
        super().finish()
        self.event.set()
        sk: socket.socket = self.request
        logging.info('del:{}'.format(sk))
        clients.remove(sk)
        self.request.close()


if "__main__" == __name__:
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 80), sever_Handler)
    threading.Thread(target=server.serve_forever, name="tcp server.").start()

    while True:
        cmd = input(">>>")
        if cmd.strip() == "quit":
            server.shutdown()
            # server.server_close()
            break
        logging.info(threading.enumerate())
