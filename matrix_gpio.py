#!/usr/bin/env python
# -*- coding: utf-8 -*-

' an Gpio module '

__author__ = 'kaixi fan'

import os
import sys
import time
import matrix_logger as mlog

#class Gpio
#       List all GPIOs here. These GPIO could be usesd as led or button.
#       They are initialized int board_init module.
#   
class Gpio(object):
    #private data:
    #GPIOs map
    #GPIOA - 0, GPIOB - 32
    __gpio_map = {
                'gpio_a2': '2',
                'gpio_a3': '3',
                'gpio_a6': '6',
                'gpio_a17': '17',
                'gpio_c0': '64',
                'gpio_c1': '65',
                'gpio_c2': '66',
                'gpio_c3': '67',
                'gpio_g8': '200',
                'gpio_g9': '201',
                'gpio_g11': '203',
                'gpio_l11': '331',    
                };
    #GPIO dir           
    __gpio_dir = '/sys/class/gpio'
    __gpio_direction = ''
    __gpio_value = ''

    def __init__(self, gpio_name):
        # Creat log
        self.__logger = mlog.MatrixLogger("Gpio")
        
        if self.__gpio_map.has_key(gpio_name):
            self.__gpio_dir = os.path.join(self.__gpio_dir, 'gpio' + self.__gpio_map[gpio_name])
            self.__gpio_direction = os.path.join(self.__gpio_dir, 'direction')
            self.__gpio_value = os.path.join(self.__gpio_dir, 'value')
        else:
            self.__logger.error("unknown gpio %s", gpio_name)
            return -1

    # set gpio direction
    # direction is a string, should be 'output' or 'input'.
    def set_direction(self, direction):
        if direction == 'output':
            cmdstr = "echo 'out' > " + self.__gpio_direction
        else if direction == 'input':
            cmdstr = "echo 'in' > " + self.__gpio_direction
        else:
            self.__logger.error("unknown input %s", direction)
            return -1
            
        os.system(cmdstr)
        
    # set gpio output value
    # value is a string, should be '0' or '1'.
    def set_value(self, value):
        if value == '0':
            cmdstr = 'echo 0 > ' + self.__gpio_value 
        else if value == '1':
            cmdstr = 'echo 1 > ' + self.__gpio_value
        else:
            self.__logger.error("unknown input %s", direction)
            return -1
            
        os.system(cmdstr)
        
        return 0

    # get gpio value
    # value is a string, should be '0' or '1'
    def get_value(self):      
        try:
            fd = open(self.__gpio_value, 'r')
        except IOError,e:
            self.__logger.error("error: fail to open %s", self.__gpio_value)
            return -1
        else:
            value = fd.read()
            fd.close()
            return value
            
 
