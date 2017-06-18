#!/usr/bin/env python
# -*- coding: utf-8 -*-

' an led module '

import os
import sys
import time
import logging
from logging.handlers import TimedRotatingFileHandler


class MatrixLogger(object):

    def __init__(self, name):
        log_file_path = './log/matrix/'
        if os.path.isdir(log_file_path):
            pass
        else:
            os.makedirs(log_file_path)

        # 通过下面的方式进行简单配置输出方式与日志级别
        # 创建一个logger
        self.__logger = logging.getLogger('mylogger')
        self.__logger.setLevel(logging.DEBUG)

        # 日志打印格式
        log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
        formatter = logging.Formatter(log_fmt)

        # 创建TimedRotatingFileHandler对象
        log_file_name = log_file_path + name + '.log'
        log_file_handler = TimedRotatingFileHandler(filename=log_file_name, when="M", interval=3, backupCount=3)
        # log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
        log_file_handler.setFormatter(formatter)
        logging.basicConfig(level=logging.DEBUG)

        # 给logger添加handler
        self.__logger.addHandler(log_file_handler)

        # 记录第一条日志
        self.__logger.info('第一条打印消息.')

    def debug(self, *args, **kwargs):
        self.__logger.debug(args)

    def info(self, *args, **kwargs):
        self.__logger.info(args)

    def warn(self, *args, **kwargs):
        self.__logger.warn(args)

    def error(self, *args, **kwargs):
        self.__logger.error(args)

    def critical(self, *args, **kwargs):
        self.__logger.critical(args)