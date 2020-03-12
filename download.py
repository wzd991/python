#!usr/bin/env python
# -*- coding:utf-8 -*-
import urllib.request
import re
import traceback
import binascii
import sys
from bs4 import BeautifulSoup

class get_file_url(object):
    def __init__(self):
        self.url_list = ''
        pass
    def get_url_path(self):
        url = ''
        for val in self.url_list:
            url += val
        return url

    def get_file_name(self):
        self.url_list = ['http://windsbridge.cn:86/']

        while True:
            try:
                addr = self.get_url_path()
                print(addr)
                response = urllib.request.urlopen(addr)
                html_doc = response.read()
                # 创建一个BeautifulSoup解析对象
                soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
                # 获取所有的链接

                links = soup.find_all('a')
                idx = 0
                link_name = []
                for link in links:
                    if link.name == 'a' :
                        if link['href'][-1] == '/' or  link['href'][-4:] == '.bin':
                            link_name.append(link)
                            print('%2d %s'%(idx, link['href']))
                            idx += 1

                del soup
                del response

                temp = input('输入序号:')

                try:
                    val = int(temp)

                    if val < len(link_name):
                        if link_name[val]['href'] == '../' :
                            if len(self.url_list) > 1:
                                del self.url_list[-1]
                        elif link_name[val]['href'][-4:] == '.bin':
                            self.url_list.append(link_name[val]['href'])
                            return self.get_url_path()
                        else:
                            self.url_list.append(link_name[val]['href'])

                    else:
                        print('输入错误< {}'.format(idx))
                except Exception as e:
                    print('输入错误', e)
            except Exception as e:
                print(e)
                print(traceback.print_exc())
                return None
if __name__ == '__main__':
    try:
        hd = get_file_url()
        name = hd.get_file_name()
        response = urllib.request.urlopen(name)
        data = response.read(1024*1024*4)
        del response
        print(len(data))
        print(type(data))
    except Exception as e:
        print(e)
# print(binascii.hexlify(data))
