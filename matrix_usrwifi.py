#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import serial
import logging
import matrix_logger as mlog

class UsrWifi:
    def __init__(self):
        # Creat log
        self.__logger = mlog.MatrixLogger("UsrWifi.log")
        
        # Open serial port
        self.__logger.info("open /dev/ttyS1 .")
        self.__ser = serial.Serial('/dev/ttyS1',115200, timeout=1)
        self.__mode = 'AT' #wifi module modle
        self.__ackLen = 50 #ack length from wifi module

    ###########################
    # Initialize wifi module
    ###########################
    def init(self):
        self.setModeSta()
        self.setTcps("192.168.199.1", "8100")
        self.saveDefaultParas()
        self.reset()    

    ###########################
    # Enter AT command mode
    ###########################
    def enterAt(self):
        #first step, send '+++' to module
        self.__ser.write('+')
        time.sleep(0.01)
        self.__ser.write('+')
        time.sleep(0.01)
        self.__ser.write('+')
        time.sleep(0.4)
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from +++:\r\n%s', value)
        if cmp(value, 'a') != 0:
            self.exitAt()
            return False
            
        #second step, send 'a' to module
        self.__ser.write('a')
        time.sleep(0.2)
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from a:\r\n%s', value)

        if value.find('OK') != -1:
            return True
        else:
            self.exitAt()
            return False

    ###########################
    # Exit AT command mode
    ###########################
    def exitAt(self):
        self.__ser.write('AT+ENTM\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s' , value)
        


    ###########################
    # 设置当前参数为默认出厂参数
    ###########################
    def saveDefaultParas(self):
        self.enterAt()
    
        self.__logger.info('Send save as default parameter command !')
        self.__ser.write('AT+CFGTF\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s' , value)
        
        self.exitAt()
        
        if value.find('OK') != -1:  
            return True
        else:
            return False
            
    ###########################
    # 重启
    ###########################
    def reset(self):
        self.enterAt()
        
        self.__logger.info('Send reset command !')
        self.__ser.write('AT+Z\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s' , value)        
        
        self.exitAt()

        if value.find('OK') != -1:  
            return True
        else:
            return False
            
    ###########################
    # Set Mode as STA
    ###########################
    def setModeSta(self):
        self.enterAt()
        
        self.__logger.info('Send set sta mode command !')
        self.__ser.write('AT+WMODE=STA\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s' , value)        
        
        self.exitAt()

        if value.find('OK') != -1:  
            return True
        else:
            return False
                        
    ###########################
    # Get wifi link status
    ###########################
    def getLink(self):
        self.enterAt()

        self.__ser.write('AT+WSLK\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( '5,ack from csr322 module:\r\n%s' , value)
        
        self.exitAt()
        
        index = value.find('+OK')
        if index == -1:
            return False
        index += 4
        if value.find('DISCONNECTED') != -1:
            self.exitAt()
            return 0
        else:
            return 1

    ###########################
    # Set UART0 socket as TCP server:
    # ip = "local ip"
    # port = "8100"
    ###########################
    def setTcps(self, ip, port):
        self.enterAt()

        self.__ser.write('AT+WKMOD=TRANS\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( 'ack from csr322 module:\r\n%s', value)
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return False
        
        cmd = 'AT+SOCKA=TCPS' + ','
        cmd += ip + ',' + port + '\r'
        self.__logger.info( 'cmd = %s' , cmd)
        self.__ser.write(cmd)
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s' , value)
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return False
        
        time.sleep(2)
        self.exitAt()
        
        return True


    ####################################
    # tx data.
    # return:
    #   True    -   data tx finished
    #   False   -   internet connection is broken   
    ####################################
    def txData(self, data):
        ret = self.getTcpLink()
        if ret == 0:
            return False

        self.__ser.write(data)

        return True

    ####################################
    # rx data from tcp or http connections
    # return:
    #   data
    #   False   internet connection is broken
    ####################################
    def rxData(self):
        ack = ''
        while 1:
            value = self.__ser.read(self.__ackLen)
            ack += value
            self.__logger.info('return from remote:\r\n %s' , value)
            if value == '':
                break

        return ack

    ####################################
    # 读取TCP link状态
    ####################################
    def getTcpLink(self):
        self.enterAt()

        self.__ser.write('AT+SOCKLKA\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s' , value)
        
        self.exitAt()
        
        index = value.find('+OK')
        if index == -1:
            return False

        index += 4
        stat = value[index:]
        self.__logger.info('tcp link stat :\r\n%s' , stat)
        if stat.find('DISCONNECTED') != -1:
            return 0
        elif stat.find('CONNECTED') != -1:
            return 1
        else:
            return 2
    
