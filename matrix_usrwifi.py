#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import serial
import logging

class UsrWifi:
    def __init__(self):
        self.__ser = serial.Serial('/dev/ttyUSB0',115200, timeout=1)
        self.__mode = 'AT' #wifi module modle
        self.__ackLen = 50 #ack length from wifi module
        
        # 通过下面的方式进行简单配置输出方式与日志级别
        # 创建一个logger
        self.__logger = logging.getLogger('mylogger')
        self.__logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler('UsrWifi.log')
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

    def enterAt(self):
        #first step, send '+++' to module
        self.__ser.write('+')
        time.sleep(0.01)
        self.__ser.write('+')
        time.sleep(0.01)
        self.__ser.write('+')
        time.sleep(0.4)
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from +++:\r\n%s' , value)
        if cmp(value, 'a') != 0:
            self.exitAt()
            return False
	#second step, send 'a' to module
        self.__ser.write('a')
        time.sleep(0.2)
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from a:\r\n%s' , value)

        if value.find('OK') != -1:
            return True
        else:
            self.exitAt()
            return False

    def exitAt(self):
        self.__ser.write('AT+ENTM\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s' , value)

    def reset(self):
        self.__ser.write('AT+Z\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s' , value)
        self.__logger.info('reset module.')
    
    def resetModule(self):
        self.enterAt()
        self.reset()
        time.sleep(5)

    def getVersion(self):
        self.enterAt()

        self.__ser.write('AT+VER\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s' , value)
        
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return 0
        index += 4
        ver = value[index:]
        ver = ver.strip()    

        self.exitAt()
        return ver

    #################
    # setMode('STA')
    # setMode('AP')
    #################
    def setMode(self, mode):
        cmd = 'AT+WMODE='
        if mode == 'STA':
            cmd += 'STA\r'
        elif mode == 'AP':
            cmd += 'AP\r'
        else:
            return False

        self.enterAt()
        self.__ser.write(cmd)

        value = self.__ser.read(self.__ackLen)
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return False
        else:
            self.exitAt()
            return True

    def getMode(self):
        self.enterAt()

        self.__ser.write('AT+WMODE\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s' , value)
        
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return 0
        index += 4
        mode = value[index:]
        self.__logger.info('mode == %s' , mode)    

        self.exitAt()


    ################################
    # When module is in 'STA' mode,
    # set wifi name and password.
    #
    # ssid  -   string
    # pwd   -   string
    ################################
    def setStat(self, ssid, pwd):
        self.enterAt()

        cmd = 'AT+WSTA='
        cmd += ssid
        cmd += ','
        cmd += pwd
        cmd += '\r'
        self.__ser.write(cmd)

        value = self.__ser.read(self.__ackLen)
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return False
        else:
            self.exitAt()
            return True
    
    ################################
    #
    #   get ap ssid and password
    ################################
    def getStat(self):
        self.enterAt()

        self.__ser.write('AT+WSTA\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( '5,ack from csr322 module:\r\n%s' , value)
        
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return False
        index += 4
        stat =  value[index:]
        wifi = stat.strip()
        wifi = wifi.split(',')
        
        self.exitAt()
        return wifi

    
    ################################
    # When module is in 'STA' modle, 
    # set ip address.
    #
    # 
    ################################
    def setDhcpIp(self):
        self.enterAt()

        cmd = 'AT+WANN='
        cmd += 'DHCP'
        cmd += '\r'
        self.__ser.write(cmd)

        value = self.__ser.read(self.__ackLen)
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return False
        else:
            self.exitAt()
            return True

    def setStaticIp(self, ip, mask, gateway, dns):
        self.enterAt()

        cmd = 'AT+WANN='
        cmd += 'STATIC' + ',' + ip + ',' + mask + ',' + gateway + ',' + dns + '\r'
        self.__ser.write(cmd)

        value = self.__ser.read(self.__ackLen)
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return False
        else:
            self.exitAt()
            return True

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

    def getWap(self):
        self.enterAt()

        self.__ser.write('AT+WAP\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( '6,ack from csr322 module:\r\n%s' , value)
        
        index = value.find('+OK')
        if index != -1:
            self.exitAt()
            return 0

    #########################
    # get wifi channel number
    #########################
    def getChl(self):
        self.enterAt()
        self.__ser.write('AT+CHANNEL\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( '6,ack from csr322 module:\r\n%s' , value)
        
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return 1000
        index += 4
        chnl = value[index:]
        chnl = chnl.strip()

        self.exitAt()
        return chnl

    ########################
    # get wifi ip in ap module
    #######################
    def getLanIp(self):
        self.enterAt()

        self.__ser.write('AT+LANN\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( '6,ack from csr322 module:\r\n%s' , value)
        
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return '255.255.255.255'

        self.exitAt()

    #######################################
    # set http client mode parameters
    #
    # 1,mode -    string
    #   "POST"
    #   "GET"
    #
    ######################################
    def setHttpcMode(self, mode):
        #step 1
        self.__ser.write('AT+WKMOD=HTPC\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( 'ack from csr322 module:\r\n%s' , value)
        index = value.find('+OK')
        if index == -1:
            return False

        #step 2
        if mode == 'GET':
            self.__ser.write('AT+HTPTP=GET\r')
        elif mode == 'POST':
            self.__ser.write('AT+HTPTP=POST\r')
        else:
            return False
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( 'ack from csr322 module:\r\n%s' , value)
        index = value.find('+OK')
        if index == -1:
            return False

        return True

    def setHttpcUrl(self, url):
        cmd = 'AT+HTPURL=' + url + '?\r'
        self.__ser.write(cmd)
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( 'ack from csr322 module:\r\n%s' , value)
        index = value.find('+OK')
        if index == -1:
            return False
        return True
        
    def setHttpcHead(self, head):
        if head =='':
            cmd = 'AT+HTPHEAD=Accept:text/html<<CRLF>>Accept-Language:zh-CN<<CRLF>>\r'
        else:
            cmd = 'AT+HTPHEAD=' + head + '\r'
        self.__ser.write(cmd)
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( 'ack from csr322 module:\r\n%s' , value)
        index = value.find('+OK')
        if index == -1:
            return False

        return True

    def setHttpcIp(self, ip, port):
        cmd = 'AT+HTPSV=' + ip + ',' + port + '\r'
        self.__ser.write(cmd)
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( 'ack from csr322 module:\r\n%s' , value)
        index = value.find('+OK')
        if index == -1:
            return False

        return True

    def setHttpcName(self, name, port):
        cmd = 'AT+HTPSV=' + name + ',' + port + '\r'
        self.__ser.write(cmd)
        value = self.__ser.read(self.__ackLen)
        self.__logger.info( 'ack from csr322 module:\r\n%s' , value)
        index = value.find('+OK')
        if index == -1:
            return False

        return True

    def initHttpc(self, ip, port):
        self.enterAt()
        self.setHttpcMode('POST')
        self.setHttpcUrl('/')
        self.setHttpcHead('')
        self.setHttpcIp(ip, port)

        self.reset()
        time.sleep(2)

        return True

    def initTcpc(self, ip, port):
        ret = self.enterAt()
        if ret == False:
            return False

        self.__ser.write('AT+WKMOD=TRANS\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s',value)
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return False
        
        cmd = 'AT+SOCKA=TCPC' + ','
        cmd += ip + ',' + port + '\r'
        self.__logger.info( 'cmd = %s' % cmd)
        self.__ser.write(cmd)
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s',value)
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return False
        
        self.reset()
        time.sleep(2)

        return True

    def initTcps(self, ip, port):
        ret = self.enterAt()
        if ret == False:
            return False

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
        
        self.reset()
        time.sleep(2)

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
        
        ret = self.getTcpLink()
        if ret == 0:
            return False

        return ack

    def getTcpLink(self):
        self.enterAt()

        self.__ser.write('AT+SOCKLKA\r')
        value = self.__ser.read(self.__ackLen)
        self.__logger.info('ack from csr322 module:\r\n%s' , value)
        index = value.find('+OK')
        if index == -1:
            self.exitAt()
            return False
        self.exitAt()
        index += 4
        stat = value[index:]
        self.__logger.info('tcp link stat :\r\n%s' , stat)
        if stat.find('DISCONNECTED') != -1:
            return 0
        elif stat.find('CONNECTED') != -1:
            return 1
        else:
            return 2
