#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import serial
import matrix_logger as mlog

class Net:
    def __init__(self):       
        # 创建一个handler，用于写入日志文件
        self.__logger = mlog.MatrixLogger('Net')


    def isLanLink(self):
        result = ""
        f = open("/sys/class/net/wlan0/operstate")               # 返回一个文件对象 
        line = f.readline()                                      # 调用文件的 readline()方法
        while line:
            result = result + line
            line = f.readline()
        f.close() 
        
        if result.find('up') == -1:
            return False
        else:
            return True
           
    def isWanLink(self):
        result = self.isLanLink()
        if result == False:
            return False
        os.system('wget http://www.baidu.com/ -P /root')
        ret = os.path.isfile('/root/index.html')
        if result:
            os.system('rm -f /root/index.html')
            self.__logger.info('wan is link up. ')
            return True
        else:
            self.__logger.info('wan is link down. ')
            return False
                            