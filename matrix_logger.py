#!/usr/bin/env python
# -*- coding: utf-8 -*-

' an led module '

__author__ = 'kaixi fan'

import os
import sys
import time
import logging
import os

class MatrixLogger(object):

    def __init__(self, name):
        #删除log文件
        os.system('rm -rf ~/matrixlog/*')
        
        # 通过下面的方式进行简单配置输出方式与日志级别
        # 创建一个logger
        self.__logger = logging.getLogger('mylogger')
        self.__logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        logfile = "~/matrixlog/" + name
        fh = logging.FileHandler(name)
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
        
    def info(self, message):
        self.__logger.info(message)