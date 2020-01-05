#!usr/bin/env python
# -*- coding: UTF-8 -*-
#logging test
import sys
import logging
import time
import datetime
import logging.handlers
# %(levelno)s：打印日志级别的数值
# %(levelname)s：打印日志级别的名称
# %(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
# %(filename)s：打印当前执行程序名
# %(funcName)s：打印日志的当前函数
# %(lineno)d：打印日志的当前行号
# %(asctime)s：打印日志的时间
# %(thread)d：打印线程ID
# %(threadName)s：打印线程名称
# %(process)d：打印进程ID
# %(message)s：打印日志信息

def get_timestr():
	import time
	import datetime
	localtime = time.localtime(time.time())
	now = '%04d-%02d-%02d %02d:%02d:%02d'%(localtime.tm_year,
		localtime.tm_mon, localtime.tm_mday, localtime.tm_hour,
		localtime.tm_min, localtime.tm_sec)
	return now

formatter = logging.Formatter('%(asctime)s %(filename)s %(name)s %(levelname)s %(funcName)s: %(levelno)d %(message)s')
logger = logging.getLogger('main')
logger.setLevel(level=logging.DEBUG)
handler1 = logging.handlers.RotatingFileHandler('sys.log',maxBytes=1024*1024*100,backupCount=10,encoding="utf-8",delay=False)
handler1.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logger.addHandler(console)
logger.addHandler(handler1)
logger.info(get_timestr())
log_max = 100000
while log_max:
	log_max-=1
	logger.info(get_timestr())
	time.sleep(1)