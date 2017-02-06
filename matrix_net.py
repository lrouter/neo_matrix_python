#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import serial
import logging

class Net:
    def __init__(self):       
        # 通过下面的方式进行简单配置输出方式与日志级别
        # 创建一个logger
        self.__logger = logging.getLogger('mylogger')
        self.__logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler('Net.log')
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.__logger.addHandler(fh)
        self.__logger.addHandler(ch)

        # 记录一条日志
        self.__logger.info('first message.')
        
    def isLanLink(self):
        self.__logger.info('isLanLink(). ')
        
        result = ""
        f = open("/sys/class/net/wlan0/operstate")               # 返回一个文件对象 
        line = f.readline()                                      # 调用文件的 readline()方法
        while line:  
              self.__logger.info('read from /sys/class/net/wlan0/operstate: %s\n', line)  
              result = result + line
              line = f.readline()  
        f.close() 
        
        if result.find('up') == -1:
           return False 
        else:
           return True
           
    def isWanLink(self):
        self.__logger.info('isWanLink(). ')
        
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
                            