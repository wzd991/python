#!usr/bin/env python
# -*- coding:UTF-8 -*-

from __future__ import  absolute_import
from queue import *
import  os
import sys
import threading
import re
import serial
from serial.tools.list_ports import comports
import struct
import binascii
import time
import datetime
import select
import atexit
import logging
import logging.handlers
import logging.config
CTRL_A = 1
CTRL_B = 2
CTRL_C = 3
CTRL_D = 4
CTRL_E = 5
CTRL_F = 6
CTRL_G = 7
CTRL_H = 8
logging.basicConfig(format="%(levelname)s %(asctime)s %(lineno)d %(message)s",stream=sys.stdout,level=logging.DEBUG)

def get_uart_name():
    while True:
        sys.stdout.write("\033[2J")
        sys.stdout.write('\033[0;0H')
        port_list = []
        index = 0
        print('串口序号表')
        print('=================================')
        for n, (port,desc, hwid) in enumerate(sorted(comports()),1):
            port_list.append(port)
            print('序号:{} 名称{}'.format(index, port))
            index+=1
        print('==================================')
        if len(port_list) == 0:
            print('Please connect uart to computer.')
            sys.exit()

        try:
            id = input('序号:')
            if type(id) == str:
                try:
                    id = int(id)
                except:
                    continue
                if id < len(port_list):
                    return  port_list[id]
                else:
                    print('2:id < {}'.format(len(port_list)))
            else:
                print('1:id < {}'.format(len(port_list)))
        except KeyboardInterrupt:
            sys.eixt()
        except:
            sys.exit()

def get_arg_list(data):
    ret = []
    temp = data.split(' ')

    for val in temp:
        if val.find(',') == -1:
            ret.append(val)
        else:
            temp1 = val.split(',')
            for val1 in temp1:
                val1 = val1.replace('"', '')
                ret.append(val1)
    return (ret,len(ret))

AT_DECODE_MODE_AT =1
AT_DECODE_MODE_REC = 2
AT_DECODE_MODE_SEND =3
class main_fun():
    def __init__(self, uart_name):
        self.at_chche = bytearray()
        self.at_msg_list = []
        self.apn = ''
        self.uart_hd = None
        self.time_cnt = 0
        self.server_connect_cnt = 0
        self.send_temp = ''
        self.decode_mode = AT_DECODE_MODE_AT
        self.rec_msg_cnt = 0
        self.connect_id = None
        self.send_to_server_data = None
        self.apn_code_dir = {
            '46000': 'cmnet',
            '46002': 'cmnet',
            '46007': 'cmnet',
            '46008': 'cmnet',
            '46004': 'cmmtm',
            '46001': '3gnet',
            '46006': '3gnet',
            '46009': '3gnet',
            '46003': 'ctnet',
            '46005': 'ctnet',
            '46011': 'ctnet'}
        self.exit_event = threading.Event()
        self.time_dir = {}
        self.time_hd = threading.Thread(target=self.time_fn, name= 'timer')
        self.time_hd.daemon = True
        self.time_hd.start()
        try:
            self.uart_hd = serial.serial_for_url(uart_name, 115200, parity='N',
                                        rtscts=False, xonxoff=False,do_not_open=True)
            self.uart_hd.open()
        except Exception as e:
            print(e)
            sys.exit()

        self.uart_send("AT\r")
        self.time_start(1,1,True,self.time_test1)
        # self.time_start(2,100, True, self.time_test2)
        while True:
            try:
                data = self.uart_hd.read(1)
                # logging.debug(data)
                self.at_decode(data)
            except Exception as e:
                print(e)
                print('exit')
                sys.exit()

    def time_start(self,id, ten_ms, period, fn):
        if ten_ms == 0 or period > 1:
            logging.error('not support parm:{}{}{}{}'.format(id,ten_ms,period,fn))
            return
        self.time_dir[id] = [ten_ms,ten_ms, period,fn]

    def time_stop(self,id):
        if id in self.time_dir.keys():
            del self.time_dir[id]

    def send_to_server(self,data):
        if self.decode_mode == AT_DECODE_MODE_AT:
            if type(data) == str:
                self.send_to_server_data = data.encode()
            elif type(data) == bytearray:
                self.send_to_server_data = bytes(data)
            elif type(data) == bytes:
                self.send_to_server_data = data
            self.uart_send('AT+CIPSEND=1,%d\r' % (len(data)))
            self.decode_mode = AT_DECODE_MODE_SEND

    def time_fn(self):
        while True:
            rm_dir = []
            if len(self.time_dir):
                for time_id, val in self.time_dir.items():
                    if val[0]:
                        val[0] -= 1
                    if val[0] == 0:
                        val[3](time_id)
                        if val[2]:
                            val[0] = val[1]
                        else:
                            rm_dir.append(time_id)

                if len(rm_dir):
                    for time_id in rm_dir:
                        del self.time_dir[time_id]
            time.sleep(0.01)
            pass
        pass
    def time_test1(self,time_id):
        # logging.debug('time:{}'.format(time_id))
        self.time_cnt+=1

    def time_test2(self,time_id):
        logging.debug('id:{} cnt:{}'.format(time_id, self.time_cnt))
        pass
    def uart_send(self, data):
        self.send_temp = data[:-1]
        self.uart_hd.write(data.encode())
        self.uart_hd.flush()

    def at_msg_fn(self):
        (send_msg, send_msg_cnt) = get_arg_list(self.send_temp)
        logging.debug('t:{} LINK:{} req:{} IND:{}'.format(self.time_cnt, self.server_connect_cnt, send_msg,self.at_msg_list))
        for temp in self.at_msg_list:
            (arg,cnt) = get_arg_list(temp)
            if cnt == 0:
                return

            # logging.debug('t:{} connect cnt:{} arg:{}'.format(self.time_cnt, self.server_connect_cnt, arg))
            if arg[0][:4] == '+IPD':
                self.decode_mode = AT_DECODE_MODE_REC
                self.rec_msg_cnt = int(arg[0][4:])
                self.at_chche = bytearray()
                logging.debug('cnt:{}'.format(self.rec_msg_cnt))
                return

            elif arg[0] == '+IPCLOSE:':
                self.uart_send('AT\r')
                self.connect_id = None
                return
            elif arg[0] == '+CME':
                if arg[1] == 'ERROR:':
                    time.sleep(3)
                    self.uart_send('AT+CFUN=0\r')
                return
            elif arg[0] == '+CIPSEND:':
                return

            if send_msg[0] == 'AT+CFUN=0':
                time.sleep(4)
                self.uart_send('AT+CFUN=1\r')
            elif send_msg[0] == 'AT+CFUN=1':
                self.uart_send('AT\r')
            elif send_msg[0] == 'AT':
                if arg[0] == 'OK':
                    self.uart_send("ATE0\r")
            elif send_msg[0] == 'ATE0':
                if arg[0] == 'OK':
                    self.uart_send("AT+CPIN?\r")
            elif send_msg[0] == 'AT+CPIN?':
                if arg[0] == '+CPIN:':
                    if arg[1] == 'READY':
                        self.uart_send("AT+CIMI\r")
            elif send_msg[0] == 'AT+CIMI':
                if arg[0][:3] == '460':
                    mmc = arg[0][:5]
                    if mmc in self.apn_code_dir.keys():
                        self.apn = self.apn_code_dir[mmc]
                        self.uart_send('AT+CGDCONT?\r')
                    logging.debug('mmc:{} apn:{}'.format(mmc, self.apn))
                pass
            elif send_msg[0] == 'AT+CGDCONT?':
                if arg[0] == '+CGDCONT:' and arg[2] == 'IP':
                    if arg[3] == self.apn:
                        self.uart_send("AT+CSQ\r")
                    else:
                        self.uart_send('AT+CGDCONT=1,"IP","%s"\r' % (self.apn))
                pass
            elif send_msg[0] == 'AT+CGDCONT=1':
                time.sleep(1)
                self.uart_send("AT+CSQ\r")
            elif send_msg[0] == 'AT+CSQ':
                try:
                    if arg[0] == '+CSQ:':
                        self.uart_send('AT+CPSI?\r')
                except:
                    pass

            elif send_msg[0] == 'AT+CPSI?':
                if arg[0] == '+CPSI:':
                    self.uart_send("AT+NETOPEN?\r")
            elif send_msg[0] == 'AT+NETOPEN?':
                if arg[0] == '+NETOPEN:':
                    if arg[1] == '0':
                        self.uart_send("AT+NETOPEN\r")
                    elif arg[1] == '1':
                        self.uart_send("AT+CIPOPEN?\r")
            elif send_msg[0] == 'AT+NETOPEN':
                if cnt == 2:
                    if arg[1] == '0':
                        self.uart_send("AT+CIPOPEN?\r")
                pass
            elif send_msg[0] == 'AT+CIPOPEN?':
                if arg[0] == '+CIPOPEN:':
                    idx = int(arg[1])

                    if cnt > 2:
                        self.connect_id = idx
                    if idx == 9:
                        if self.connect_id == None:
                            # self.uart_send('AT+CIPOPEN=1,"TCP","222.249.238.19",52012\r')
                            self.uart_send('AT+CIPOPEN=1,"TCP","222.249.238.19",52011\r')
                        else :
                            logging.info('server connect ok.')
                            self.send_to_server('123456')
                            self.time_start(3,100,True,self.heart_fn)
                            # self.uart_send('AT+CIPCLOSE=1\r')
                            # self.uart_send('AT+CFUN=0\r')

            elif send_msg[0] == 'AT+CIPOPEN=1':
                if arg[0] == '+CIPOPEN:':
                    logging.info('hd:{} st:{}'.format(arg[1], arg[2]))
                    if arg[2] == '0':
                        self.server_connect_cnt+=1
                        logging.info('server connect ok.')
                        self.send_to_server('12345')
                        self.time_start(3, 100, True, self.heart_fn)
                    else:
                        logging.debug('fail')
                        time.sleep(1)
                        self.uart_send('AT\r')

    def heart_fn(self,time_id):
        msg = 'time:{}'.format(self.time_cnt*100)
        self.send_to_server(msg)

    def at_decode(self, val):
        for temp in val:
            if self.decode_mode == AT_DECODE_MODE_AT:
                if temp == 0x0d or temp == 0x0a:
                    if len(self.at_chche):
                        msg = self.at_chche.decode()
                        self.at_msg_list.append(msg)
                        (send_msg, send_msg_cnt) = get_arg_list(self.send_temp)
                        if msg == 'OK' or msg == 'ERROR' or send_msg[0] == 'AT+NETOPEN' or \
                                (len(send_msg[0]) > 8 and send_msg[0][:8] == '+CIPOPEN'):
                            self.at_msg_fn()
                            self.at_msg_list = []
                        self.at_chche = bytearray()
                else:
                    self.at_chche.append(temp)
            elif self.decode_mode == AT_DECODE_MODE_REC:
                self.at_chche.append(temp)
                if len(self.at_chche) == self.rec_msg_cnt + 2:
                    del self.at_chche[0]
                    del self.at_chche[-1]
                    print(binascii.hexlify(self.at_chche))
                    self.at_chche = bytearray()
                    self.decode_mode = AT_DECODE_MODE_AT
                pass
            elif self.decode_mode == AT_DECODE_MODE_SEND:
                if temp == 0x3e:
                    # logging.debug(temp)
                    self.uart_hd.write(self.send_to_server_data)
                    self.decode_mode = AT_DECODE_MODE_AT

if __name__ == '__main__':
    # choose_prot = get_uart_name()
    choose_prot = 'COM3'
    exit_event = threading.Event()
    print(choose_prot)
    fun = main_fun(choose_prot)
