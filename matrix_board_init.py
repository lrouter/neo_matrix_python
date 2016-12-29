#!/usr/bin/env python
# -*- coding: utf-8 -*-

' an led module '

__author__ = 'kaixi fan'

import os
import sys
import time

##############################################################
# 				Board init function	
##############################################################
def board_init():
    
    ##
    ##creat gpio inode in sysfs filesystem
    ##
    gpio_dir = '/sys/class/gpio'
    gpio_export_dir = os.path.join(gpio_dir, 'export')
    led_upload_dir = os.path.join(gpio_dir, 'gpio203')
    led_usrcfg_0_dir = os.path.join(gpio_dir, 'gpio66')
    led_usrcfg_1_dir = os.path.join(gpio_dir, 'gpio67')
    button_phtoto_dir = os.path.join(gpio_dir, 'gpio64')
    button_restore_dir = os.path.join(gpio_dir, 'gpio65')
    
    cmdstr = 'chmod 700 ' + gpio_export_dir
    os.system(cmdstr)
    
    #led upload
    if os.path.exists(led_upload_dir):
       pass
    else:
       cmdstr = 'echo 203 > ' + gpio_export_dir
       os.system(cmdstr)
       
    #led usrcfg_0
    if os.path.exists(led_usrcfg_0_dir):
       pass
    else:
       cmdstr = 'echo 66 > ' + gpio_export_dir
       os.system(cmdstr)
       
    #led usrcfg_1
    if os.path.exists(led_usrcfg_1_dir):
       pass
    else:
       cmdstr = 'echo 67 > ' + gpio_export_dir
       os.system(cmdstr)
       
    #button for photo
    if os.path.exists(button_phtoto_dir):
       pass
    else:
       cmdstr = 'echo 64 > ' + gpio_export_dir
       os.system(cmdstr)

    #button for resetting to factory state
    if os.path.exists(button_restore_dir):
       pass
    else:
       cmdstr = 'echo 65 > ' + gpio_export_dir
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
def boad_uninit():
    #delet releated file inode in sysfs filesystem
    gpio_dir = '/sys/class/gpio'
    gpio_unexport_dir = os.path.join(gpio_dir, 'unexport')
    led_upload_dir = os.path.join(gpio_dir, 'gpio203')
    led_usrcfg_0_dir = os.path.join(gpio_dir, 'gpio66')
    led_usrcfg_1_dir = os.path.join(gpio_dir, 'gpio67')
    button_phtoto_dir = os.path.join(gpio_dir, 'gpio64')
    button_restore_dir = os.path.join(gpio_dir, 'gpio65')
    
    cmdstr = 'chmod 700 ' + gpio_unexport_dir
    os.system(cmdstr)
    
    #led upload
    if os.path.exists(led_upload_dir):
       cmdstr = 'echo 203 > ' + gpio_unexport_dir
       os.system(cmdstr)
       
    #led usrcfg_0
    if os.path.exists(led_usrcfg_0_dir):
       cmdstr = 'echo 66 > ' + gpio_unexport_dir
       os.system(cmdstr)
       
    #led usrcfg_1
    if os.path.exists(led_usrcfg_1_dir):
       cmdstr = 'echo 67 > ' + gpio_unexport_dir
       os.system(cmdstr)
       
    #button for photo
    if os.path.exists(button_phtoto_dir):
       cmdstr = 'echo 64 > ' + gpio_unexport_dir
       os.system(cmdstr)

    #button for resetting to factory state
    if os.path.exists(button_restore_dir):
       cmdstr = 'echo 65 > ' + gpio_unexport_dir
       os.system(cmdstr)

                                  
    ##
    ##delet adxl34x inode in sysfs filesystem
    ##
    adxl34x_dir = '/sys/bus/i2c/drivers/adxl34x'
    if os.path.exists(adxl34x_dir):
       os.system('modprobe -r adxl34x')
       os.system('modprobe -r adxl34x-i2c') 
                            