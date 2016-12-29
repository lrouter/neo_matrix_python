#!/usr/bin/env python
# -*- coding: utf-8 -*-

' an led module '

__author__ = 'kaixi fan'

import os
import sys
import time

#class Led
#       ledname:
#           -   led_upload
#           -   led_usrcfg_0
#           -   led_usrcfg_1
#
#   
class Led(object):
    #private data:
    #   __led_name: led name
    #   __led_status: led status, on or off
    __led_name = 'led_upload'
    __status =  'off'

    def __init__(self, led_name):
        led_dir = '/sys/class/gpio'
        if led_name == 'led_upload':
            self.__led_name = led_name
            self.__led_dir = os.path.join(led_dir, 'gpio203')
        elif led_name == 'led_usrcfg_0':
            self.__led_name = led_name
            self.__led_dir = os.path.join(led_dir, 'gpio66')
        elif led_name == 'led_usrcfg_1':
            self.__led_name = led_name
            self.__led_dir = os.path.join(led_dir, 'gpio67')
        else:
            print 'unknown led name %s' % led_name
            return -1

        self.__led_dirt_dir = os.path.join(self.__led_dir, 'direction')
        self.__led_val_dir = os.path.join(self.__led_dir, 'value')
	
	print self.__led_dirt_dir
	print self.__led_val_dir

    #set led on
    def set_on(self):
        cmdstr = 'echo \'out\' > '+ self.__led_dirt_dir
        os.system(cmdstr)
        cmdstr = 'echo \'0\' > ' + self.__led_val_dir
        os.system(cmdstr)
        
        self.__status = 'on'
        
        return 0

    #set led off
    def set_off(self):
        cmdstr = 'echo \'out\' > '+ self.__led_dirt_dir
        os.system(cmdstr)
        cmdstr = 'echo \'1\' > ' + self.__led_val_dir
        os.system(cmdstr)

        self.__status = 'off'

        return 0

    #get led status
    def get_status(self):        
        cmdstr = 'echo \'out\' > '+ self.__led_dirt_dir
        os.system(cmdstr)

        try:
            fd = open(self.__led_val_dir)
        except IOError,e:
            print 'error: fail to open %s' % self.__led_val_dir
            return -1
        else:
            self.__status = fd.read()
            fd.close()
            return self.__status
            
 
