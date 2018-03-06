#!/usr/bin/env python
# -*- coding: utf-8 -*-

' an board init module '

__author__ = 'kaixi fan'

import os
import sys
import time
import matrix_logger as mlog

class BoardInit(object):
		
		#GPIOs map
		#GPIOA - 0, GPIOB - 32
		__gpio_map = {'led_upload': '203',
					'led_usrcfg_0': '66',
					'led_usrcfg_1': '67',
					'button_phtoto': '64',
					'button_restore': '65',
					'gpio_a3': '3',
					'gpio_a6': '6',
					'gpio_a17': '17',
					'gpio_g8': '200',
					'gpio_g9': '201'
					};
		#GPIO dir			
        __gpio_dir = '/sys/class/gpio'
        __gpio_export_dir = '/sys/class/gpio/export'
		__gpio_unexport_dir = '/sys/class/gpio/unexport'
		
    ######################################################
    #   Method - __init__
    ######################################################    
    def __init__(self):
        # Creat log
        self.__logger = mlog.MatrixLogger("BoardInit")
        
    ##############################################################
    # 				Board init function	
    ##############################################################
    def board_init(self):
        ##
        ##creat gpio inode in sysfs filesystem
        ##

		#export GPIO pin
        cmdstr = 'chmod 700 ' + self.__gpio_export_dir
        os.system(cmdstr)
		for gpio_name, gpio_number in gpio_map.items():
			gpio_pin_dir = os.path.join(self.__gpio_dir, 'gpio' + gpio_number)
			cmdstr = 'echo ' + gpio_number + ' > ' + self.__gpio_export_dir
			if os.path.exists(gpio_pin_dir):
				pass
			else:
				os.system(cmdstr)

        ##
        ##creat adxl34x inode in sysfs filesystem
        ##
        adxl34x_dir = '/sys/bus/i2c/drivers/adxl34x'
        if os.path.exists(adxl34x_dir):
            pass
        else:
            os.system('modprobe adxl34x')
            os.system('modprobe adxl34x-i2c')


    ##############################################################
    # 				Board uninit function	
    ##############################################################
    def boad_uninit(self):

        self.__logger.info('board uninit')

        # delet releated file inode in sysfs filesystem
        cmdstr = 'chmod 700 ' + self.__gpio_unexport_dir
        os.system(cmdstr)
		for gpio_name, gpio_number in gpio_map.items():
			gpio_pin_dir = os.path.join(self.__gpio_dir, 'gpio' + gpio_number)
			cmdstr = 'echo ' + gpio_number + ' > ' + self.__gpio_unexport_dir
			if os.path.exists(gpio_pin_dir):
				os.system(cmdstr)

        #
        # delet adxl34x inode in sysfs filesystem
        #
        adxl34x_dir = '/sys/bus/i2c/drivers/adxl34x'
        if os.path.exists(adxl34x_dir):
            os.system('modprobe -r adxl34x')
            os.system('modprobe -r adxl34x-i2c')
