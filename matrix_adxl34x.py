#!/usr/bin/env python
# -*- coding: utf-8 -*-

' an adxl34x module '

__author__ = 'kaixi fan'

import os
import sys
import time

class Adxl34x(object):
    #private data
    __positon = 0.0

    def __init__(self):
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
                print 'error: adxl34x position not found' % channel
                return -1
        except OSError, e:
            print e
            return -1

        try:
            fd = open(position, 'r')
        except IOError, e:
            print 'error: fail to open %s' % position
            return -1
        else:
            __postion = fd.read()
            fd.close()
            return __postion       
