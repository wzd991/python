#!usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import serial
from serial.tools.list_ports import *
from tkinter import *
from tkinter.scrolledtext import *
from tkinter.ttk import *

class main_app():

    def __init__(self):
        self.win = Tk()
        self.win.rowconfigure(0,weight=2)
        self.win.rowconfigure(1,weight=1)
        self.win.rowconfigure(2,weight=1)
        self.rec_mode = StringVar()
        self.send_mode = StringVar()
        self.auto_line = IntVar()
        self.display_send = IntVar()
        self.display_time = IntVar()

        self.period_send_val = StringVar()
        self.period_send = StringVar()
        menu = Menu(self.win)
        menu.add_command(label='file')
        menu.add_command(label='edit')
        menu.add_command(label='tool')

        self.uart_set = LabelFrame(self.win, text='uart cfg')
        self.uart_set.grid(row=0,column=0, sticky=W+N+S+E, ipadx=5,padx=10)

        Label(self.uart_set, text='port').grid(row=0,column=0,sticky=W)
        Combobox(self.uart_set).grid(row=0, column=1,sticky=W)

        Label(self.uart_set, text='rate').grid(row=1,column=0,sticky=W)
        Combobox(self.uart_set).grid(row=1, column=1,sticky=W)

        Label(self.uart_set, text='data').grid(row=2,column=0,sticky=W)
        Combobox(self.uart_set).grid(row=2, column=1,sticky=W)
        Label(self.uart_set, text='crc').grid(row=3,column=0,sticky=W)
        Combobox(self.uart_set).grid(row=3, column=1,sticky=W)
        Label(self.uart_set, text='stop').grid(row=4,column=0,sticky=W)
        Combobox(self.uart_set).grid(row=4, column=1,sticky=W)

        Label(self.uart_set, text='cts/rts').grid(row=5,column=0,sticky=W)
        Combobox(self.uart_set).grid(row=5, column=1,sticky=W)

        self.rec_cfg = LabelFrame(self.win, text='receive set')

        self.rec_cfg.grid(row=1, column=0,ipadx=10,ipady=5,sticky=W+E+N+S,padx=10,pady=10)

        Radiobutton(self.rec_cfg, text='ascii', value=0, variable=self.rec_mode).grid(row=0,column=0,sticky=W)
        Radiobutton(self.rec_cfg, text='hex', value=1, variable=self.rec_mode).grid(row=0,column=1)

        # Checkbutton(self.rec_cfg, text='aoto line', variable=self.auto_line).grid(row=2,column=0,sticky=W)
        Checkbutton(self.rec_cfg, text='display send', variable=self.display_send).grid(row=2,column=0)
        Checkbutton(self.rec_cfg, text='display time', variable=self.display_time).grid(row=3,column=0)

        self.send_set = LabelFrame(self.win, text='send set')
        self.send_set.grid(row=2, column=0,padx=10,ipadx=5, sticky=W+N+S+E)
        Radiobutton(self.send_set, text='ascii', value=0, variable=self.send_mode).grid(row=0, column=0)
        Radiobutton(self.send_set, text='hex', value=1, variable=self.send_mode).grid(row=0, column=1)
        Checkbutton(self.send_set, text='aoto send', variable=self.period_send).grid(row=1,column=0)
        Spinbox(self.send_set,from_=0, textvariable=self.period_send_val).grid(row=1,column=1)

        self.log = Frame(self.win)
        self.log.grid(row=0, column=1,rowspan=2,padx=5,sticky=W+N+E+S)
        self.rec_text = ScrolledText(self.log)
        self.rec_text.pack(expand=True,fill=BOTH)

        self.send_frame = Frame(self.win)

        self.send_frame.grid(row=2,column= 1,padx=5,pady=10)
        self.send_text = ScrolledText(self.send_frame,height=30)
        self.send_text.grid(row=0,column=0,sticky=W+N+E+S)
        Button(self.send_frame, text='send').grid(row=0,column=1)
        self.send_list = Combobox(self.send_frame)
        self.send_list.grid(row=1,column=0, columnspan=2,sticky=W+N+E+S)
        self.win['menu'] = menu
        self.win.mainloop()
        pass

main_app()