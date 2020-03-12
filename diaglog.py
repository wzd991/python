#!usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from tkinter import *
from tkinter.scrolledtext import *
from tkinter.ttk import *

class main_win():
    def button_fn(self):
        print('button_fn')
        pass

    def check_button_fn(self):
        print('checkbutton:{} '.format(self.check_button_val.get()))
        pass
    def radio_button_fn(self):
        print(self.radio_button_val.get())

    def entry_fn(self):
        print('entry:{}'.format(self.entry_val))
    def menu_fn(self):
        print('nenu {}'.format(self.menu_radio_button_val.get()))

    def popup(self,event):
        self.menu.post(event.x_root, event.y_root)
    def __init__(self):
        self.win = Tk()
        self.check_button_val =IntVar()
        self.entry_val =StringVar()
        self.menu_radio_button_val = StringVar()
        self.labelval= StringVar()
        self.radio_button_val = StringVar()
        self.frame = Frame(self.win)
        self.frame.pack(fill=BOTH)
        Button(self.frame, text='button', command=self.button_fn).pack()
        Entry(self.frame, textvariable=self.entry_val,state=NORMAL).pack()
        self.labelval.set('nihao')
        Label(self.frame, text='lable', textvariable=self.labelval).pack()

        self.menu = Menu(self.win)
        self.menu.add_command(label='文件', command=self.menu_fn)  # 给菜单实例增加菜单项
        self.menu.add_command(label='视图', command=self.menu_fn)
        menusp = Menu(self.menu)  # 在菜单实例下创建一组子菜单
        menusp.add_command(label='子菜单1', command=self.menu_fn)  # 给这个子菜单添加菜单项
        menusp.add_command(label='子菜单2', command=self.menu_fn)
        menusp.add_checkbutton(label='checkbutton', command=self.menu_fn)
        menusp.add_radiobutton(label='radiobutton1', value=1,variable=self.menu_radio_button_val,command=self.menu_fn)
        menusp.add_radiobutton(label='radiobutton2', value=2,variable=self.menu_radio_button_val,command=self.menu_fn)
        menusp.add_radiobutton(label='radiobutton3', value=3,variable=self.menu_radio_button_val,command=self.menu_fn)
        self.menu.add_cascade(label='菜单', menu=menusp)
        self.win['menu'] = self.menu
        menu_button = Menubutton(self.win,text='nemu button')
        menu_button.pack()
        menu_button['menu'] = self.menu
        self.frame.bind("<Button-3>", self.popup)

        self.radio_but1 = Radiobutton(self.frame,text='radiobu1', value=1,variable=self.radio_button_val, command=self.radio_button_fn)
        self.radio_but2 = Radiobutton(self.frame,text='radiobu1', value=2,variable=self.radio_button_val, command=self.radio_button_fn)
        self.radio_but3 = Radiobutton(self.frame,text='radiobu1', value=3,variable=self.radio_button_val, command=self.radio_button_fn)
        self.radio_but1.pack()
        self.radio_but2.pack()
        self.radio_but3.pack()
        self.check_button_val.set(1)
        self.check_button1 = Checkbutton(self.frame,text='checkbut1', variable=self.check_button_val, command=self.check_button_fn)
        self.check_button1.pack()
        Label(self.frame,text='lable1').pack(side=LEFT)
        Label(self.frame,text='lable2').pack(side=LEFT)
        Label(self.frame,text='lable3').pack(side=RIGHT)
        win1= PanedWindow(self.frame)
        win2 = PanedWindow(win1,orient = VERTICAL)
        win1.add(win2)
        win1.pack(side=BOTTOM)
        win1.add(Label(win1,text='lablewin1'))
        win1.add(Label(win1,text='lablewin2'))
        win2.add(Label(win1,text='lablewin3'))
        win2.add(Label(win1,text='lablewin4'))
        pb = Progressbar(self.frame,orient=HORIZONTAL,length=100,value=10)
        # help((Progressbar.start))
        pb.pack()
        pb.start(interval=100)
        pb.update()
        self.spin_val = IntVar()
        Spinbox(self.frame,from_=1,to=10,increment=2,textvariable = self.spin_val).pack()
        b = Separator(self.frame, orient='horizontal')
        b.pack(fill=X)
        xx = Sizegrip()
        Combobox()
        self.win.mainloop()

class main_learn1():
    def bt1_fn(self):
        print('bt1 fn')

    def bt2_fn(self):
        print('bt2 fn')

    def __init__(self):
        self.win = Tk()
        self.win.columnconfigure(0,minsize=10, weight=10)
        self.win.columnconfigure(1, weight=20)
        self.win.rowconfigure(0, weight=3)
        self.entry1_val = StringVar()
        self.entry2_val = StringVar()
        self.log_val = StringVar()
        self.frame = LabelFrame(self.win,text='1')
        self.frame1 = LabelFrame(self.win,text='2')
        self.frame.grid(row=0, column=0, sticky=W+E+N+S)
        self.frame1.grid(row=0, column=1, sticky=W+E+N+S)
        # self.but= Button(self.frame,text='but')
        # self.but.grid(column=0, row=0, sticky=W+E+N+S)
        # self.text= ScrolledText(self.frame)
        # self.text1= ScrolledText(self.frame1)
        # self.text2= ScrolledText(self.frame1)
        # self.text.grid(column=0, row=0, sticky=W+E+N+S)
        # self.text1.grid(column=0, row=0, sticky=W+E+N+S)
        # self.text2.grid(column=1, row=0, sticky=W+E+N+S)
        # self.left_frame = Frame(self.win)
        # self.left_frame.grid(column=0, row=0,sticky=W+E+N+S)
        # self.left_frame.columnconfigure(0, weight=1)
        # self.left_frame.rowconfigure(0, weight=1)
        #
        # self.right_frame = Frame(self.left_frame)
        # self.right_frame.grid(column=1, row=0,sticky=W+E+N+S)
        # self.right_frame.columnconfigure(1, weight=1)
        # self.right_frame.rowconfigure(0,weight=1)
        # self.note_cfg = Notebook(self.left_frame)
        # self.note_cfg.grid(sticky=W+N)
        # self.cfg_frame = Frame(self.note_cfg)
        # self.note_cfg.add(self.cfg_frame, text='uart cfg')
        # Label(self.cfg_frame,text='com').grid(row=0,column=0, sticky=W+N)
        # Entry(self.cfg_frame,textvariable=self.entry1_val).grid(row=0, column=1, sticky=W+N)
        # self.bt1 = Button(self.cfg_frame, text='button1', command=self.bt1_fn)
        # self.bt1.grid(row=0, column=2, sticky=W+N)
        #
        # self.cfg_frame1 = Frame(self.note_cfg)
        # self.note_cfg.add(self.cfg_frame1, text='other')
        # Label(self.cfg_frame1,text='parity').grid(row=1, column=0, sticky=W+N)
        # Entry(self.cfg_frame1,textvariable=self.entry1_val,width=20).grid(row=1, column=1, sticky=W+N)
        # self.bt2 = Button(self.cfg_frame1,text='button2', command=self.bt2_fn)
        # self.bt2.grid(row=1,column=2, sticky=W+N)
        # self.log = ScrolledText(self.right_frame, wrap=WORD, relief = SUNKEN)
        # # help(self.log)
        # self.log.grid(row=0,column=0,sticky=W+E+N+S)

        self.win.mainloop()


main = main_win()
# main = main_win()
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
https://www.linuxidc.com/Linux/2019-08/160311.htm
'''