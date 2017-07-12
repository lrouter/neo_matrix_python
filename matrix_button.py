#!/usr/bin/env python
# -*- coding: utf-8 -*-

' an led module '

__author__ = 'kaixi fan'

import os
import sys
import time
import matrix_logger as mlog

###########################################################
# class Button
#   creator parameter:
#       ledname:
#           -   button_photo
#           -   button_restore
#
###########################################################   
class Button(object):
    # private data:

    ######################################################
    #   Method - __init__
    ######################################################    
    def __init__(self, name):
        self.__debounce = 0.02  # button debounce time, 20ms
        self.__name = 'button_photo'
        self.__status = False
        self.__button_dir = '/sys/class/gpio'

        # Creat log
        self.__logger = mlog.MatrixLogger("Button")
        
        # Creat button
        if name == 'button_photo':
            self.__name = name
            self.__dir = os.path.join(self.__button_dir, 'gpio64')
        elif name == 'button_restore':
            self.__name = name
            self.__dir = os.path.join(self.__button_dir, 'gpio65')
        else:
            self.__logger.error("unknown button name %s", name)
            return -1
        
        #set button gpio as input mode    
        self.__dirt_dir = os.path.join(self.__dir, 'direction')
        self.__val_dir = os.path.join(self.__dir, 'value')
        cmdstr = "echo 'in' > " + self.__dirt_dir
        os.system(cmdstr)


    ######################################################
    #   Method - isPressed
    #          check whether the button is pressed once
    ###################################################### 
    def isPressed(self):
        self.__status =  False
        
        try:
            fd = open(self.__val_dir, 'r')
        except IOError, e:
            self.__logger.error("error: fail to open %s", self.__val_dir)
            return -1
        else:
            input = fd.read()
            self.__logger.info("button value = %s", input)
            value = int(input)
            if value == 0:
                fd.close()
                self.__status =  True
                return True
            else:
                fd.close()
                self.__status = False
                return False
            
