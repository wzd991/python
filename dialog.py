#!usr/bin/env python
# -*- coding -*-
from tkinter import *
from tkinter.ttk import *

import threading
import sys
import time
import logging
import logging.handlers
import logging.config
import serial
logging.basicConfig(format="%(levelname)s %(asctime)s %(lineno)d %(message)s",stream=sys.stdout,level=logging.DEBUG)

#部件
'''
Button，按钮
Checkbutton，
Entry，
Frame，
Label，
LabelFrame，
Menubutton，
PanedWindow，
Radiobutton，
Scale，
Scrollbar，
Spinbox
Combobox，
Notebook， 
Progressbar，
Separator，
Sizegrip
Treeview

xscrollcommand
yscrollcommand
'''

cmd_list = (
    'AT\r',
    'AT+CSQ\r',
    'ATE0\r',
    # Request manufacturer identification
    'AT+CGMI\r',
    # Request model identification
    'AT+CGMM\r',
    # Set phone functionality
    'AT+CFUN=0\r',
    'AT+CFUN=1\r',
    'AT+CPIN?\r',
    'AT+CREG?\r',
    'AT+CPIN?\r',
    'AT+COPN?\r',
    'AT+CGREG?\r',
    'AT+CGATT?\r',
    'AT+NETOPEN?\r',
    'AT+NETCLOSE\r',
    'AT+NETOPEN\r',
    'AT+CGACT?\r',
    'AT+CGDCONT?\r',
    'AT+IPADDR?\r',
    'AT+CIPOPEN?\r',
    'AT+CDNSGIP="windsbridge.cn"\r',

)


class main_class():
    def __init__(self):
        win = Tk()
        win.title('termal')
        self.cmd_val = StringVar()
        cmd_list_hd = Combobox(win, values=cmd_list,width=70, state="readonly"
                               , textvariable=self.cmd_val)
        cmd_list_hd.pack()
        cmd_list_hd.set(cmd_list[0])
        # 按钮
        button = Button(win, text='button', command=self.button1_fn)
        button.pack()
        self.uart_hd = None
        try:
            self.uart_hd = serial.serial_for_url('COM3', 115200, parity='N',
                                        rtscts=False, xonxoff=False,do_not_open=True)
            self.uart_hd.open()
        except Exception as e:
            print(e)
            sys.exit()
        self.uart_rec_hd = threading.Thread(target=self.uart_rec_fn,name = 'uart rec')
        self.uart_rec_hd.daemon = True
        self.uart_rec_hd.start()
        win.mainloop()

    def button1_fn(self):
        val = self.cmd_val.get()
        logging.debug(val)
        self.uart_send(val)
        pass

    def uart_send(self, data):
        self.uart_hd.write(data.encode())
        self.uart_hd.flush()

    def uart_rec_fn(self):
        while True:
            try:
                data = self.uart_hd.readline()
                print(data)
            except Exception as e:
                print(e)
                print('exit')
                sys.exit()

if "__main__" == __name__:
    main_class()
