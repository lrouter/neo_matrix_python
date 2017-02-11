#!/usr/bin/env python
# -*- coding: utf-8 -*-

' an adxl34x module '

__author__ = 'kaixi fan'

import os
import sys
import time
import matrix_logger as mlog

class Adxl34x(object):
    #private data
    __positon = 0.0

    def __init__(self):
        #Creat logger
        self.__logger = mlog.MatrixLogger("Adxl34x.log")
        
        #loading driver
        self.__logger.info("loadding driver")
        os.system('modprobe adxl34x')
        os.system('modprobe adxl34x-i2c')
        self.__postion = 0.0

    def get_position(self):
        sys_dir = '/sys/bus/i2c/drivers/adxl34x'
        found = False
        try:
            for item in os.listdir(sys_dir):
                position = '%s/%s/position' % (sys_dir, item)
                if os.path.exists(position):
                    found = True
                    break;
            if not found:
                self.__logger.info("error, adxl34x position not found.")
                return -1
        except OSError, e:
            self.__logger.info("error, OSError.")
            return -1

        try:
            fd = open(position, 'r')
        except IOError, e:
            self.__logger.info("error: fail to open position")
            return -1
        else:
            __postion = fd.read()
            fd.close()
            return __postion       
