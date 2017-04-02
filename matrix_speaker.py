#!/usr/bin/env python
# -*- coding: utf-8 -*-

' an speaker module '

__author__ = 'kaixi fan'

import os
import sys
import time
import serial
import string
import matrix_logger as mlog

class Speaker(object):
    #private data
    __wackLen = 2 #write command ack length, ok
    __ackLen = 20 #read command ack length

    __cmd_ctrlDict = {'Play':       0x1, \
                     'Pause':       0x2, \
                     'PlayNext':    0x3, \
                     'PlayAbove':   0x4, \
                     'IncVolume':   0x5, \
                     'DecVolume':   0x6, \
                     'Sleep':       0x7, \
                     'Reset':       0x9, \
                     'StopPlay':    0xe, \
                     'SetVolume':   0x31, \
                     'SetEQ':       0x32, \
                     'SetPlayMode': 0x33, \
                     'ChooseMusic': 0x41, \
                     }
                     
    __cmd_reqDict = {'PlayStat':    0x10, \
                     'Volume':      0x11, \
                     'CurEQ':       0x12, \
                     'CurPlayMode': 0x13, \
                     'Version':     0x14, \
                     'NfilesInU':         0x16, \
                     'NfilesInFlash':     0x17, \
                     'PlayDev':           0x18, \
                     'MusicInU':           0x1A, \
                     'MusicInFlash':      0x1B, \
                     }
                     
    def __init__(self):
        # Creat Log
        self.__logger = mlog.MatrixLogger("Speaker.log")                
        
        # Creat serial port
        self.__ser = serial.Serial('/dev/ttyS2', 9600, timeout=0.5)  
        if not self.__ser.isOpen():
               self.__logger.info('self.__serial /dev/ttyS2 could not be opened.')
               return False


    #######################################
    ##    Make command
    #######################################
    def __makeCommand(self, cmdList):
        # Calcute checksum
        cksum = 0
        for item in cmdList:
            cksum ^= item
                          
        # make cmd
        cmd = [0x7e]
        for item in cmdList:
            cmd.append(item)
        cmd.append(cksum)
        cmd.append(0xef)

        self.__logger.info(cmd)
        #translate cmd into bytes
        cmdB = chr(cmd[0])
        i = 1
        while i < len(cmd):
            cmdB += chr(cmd[i])
            i+=1

        return cmdB
    #######################################
    ##    Play music
    #######################################    
    def play(self):
        list = [0x3]
        list.append(self.__cmd_ctrlDict['Play'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False

        time.sleep(1)
        ack = self.__ser.read(self.__wackLen)                                      

        return True
        
    #######################################
    ##    Pause play
    #######################################        
    def pause(self):
        list = [0x3]
        list.append(self.__cmd_ctrlDict['Pause'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False

        time.sleep(1)
        ack = self.__ser.read(self.__wackLen) 

        return True    

    #######################################
    ##    Play next
    #######################################        
    def playNext(self):
        list = [0x3]
        list.append(self.__cmd_ctrlDict['PlayNext'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False
        
        time.sleep(1)
        ack = self.__ser.read(self.__wackLen) 

        return True

    #######################################
    ##    Play above
    #######################################        
    def playAbove(self):
        list = [0x3]
        list.append(self.__cmd_ctrlDict['PlayAbove'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False
        time.sleep(1)
        ack = self.__ser.read(self.__wackLen) 
               
        return True
                
    #######################################
    ##    Device sleep
    #######################################        
    def sleep(self):
        list = [0x3]
        list.append(self.__cmd_ctrlDict['Sleep'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False
        time.sleep(1)
        ack = self.__ser.read(self.__wackLen) 
               
        return True   
        
    #######################################
    ##    Device return to work state
    #######################################        
    def unsleep(self):
        list = [0x3]
        list.append(self.__cmd_ctrlDict['Sleep'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.' , len, len(cmd))
               return False
        time.sleep(1)
        ack = self.__ser.read(self.__wackLen) 

        return True
        
    #######################################
    ##    Device reset
    #######################################        
    def reset(self):
        list = [0x3]
        list.append(self.__cmd_ctrlDict['Reset'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False
        time.sleep(1)
        ack = self.__ser.read(self.__wackLen) 

        return True

    #######################################
    ##    Device stop play
    #######################################        
    def stop(self):
        list = [0x3]
        list.append(self.__cmd_ctrlDict['StopPlay'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False
        time.sleep(1)
        ack = self.__ser.read(self.__wackLen) 

        return True
                
    #######################################
    ##   Set device volume
    ##   0-30 级可调
    #######################################        
    def setVolume(self, value):
        list = [0x4]
        list.append(self.__cmd_ctrlDict['SetVolume'])
        if(value > 30 or value < 0):
                  self.__logger.info('Error Paramter: volume should be 0 ~ 30, %d', value)
                  return -1
        list.append(value)
        
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False

        time.sleep(1)
        ack = self.__ser.read(self.__wackLen) 

        return True
        
    #######################################
    ##   Set device EQ
    ##   0-5(NO\POP\ROCK\JAZZ\CLASSIC\BASS)
    #######################################        
    def setEQ(self, value):
        list = [0x4]
        list.append(self.__cmd_ctrlDict['SetEQ'])
        if(value > 5 or value < 0):
                  self.__logger.info('Error Paramter: EQ should be 0 ~ 5, %d', value)
                  return -1
        list.append(value)
        
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False
        
        time.sleep(1)
        ack = self.__ser.read(self.__wackLen) 

        return True

    #######################################
    ##   Set device Play mode
    ##   0-4(全盘/文件夹/单曲/随机/无循环)
    #######################################        
    def setPlayMode(self, value):
        list = [0x4]
        list.append(self.__cmd_ctrlDict['SetPlayMode'])
        if(value > 4 or value < 0):
                  self.__logger.info('Error Paramter: play mode should be 0 ~ 4, %d', value)
                  return -1
        list.append(value)
        
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False
               
        time.sleep(1)
        ack = self.__ser.read(self.__wackLen) 

        return True
        
    #######################################
    ##   Choose music number
    ##   1-255 首(掉电记忆)
    #######################################        
    def setMusicNum(self, value):
        list = [0x5]
        list.append(self.__cmd_ctrlDict['ChooseMusic'])
        if(value > 255 or value < 1):
                  self.__logger.info('Error Paramter: musci number should be 1 ~ 255, %d', value)
                  return -1
        vh = value >> 8
        vl = value & 0xff
        list.append(vh)
        list.append(vl)
        
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False

        time.sleep(1)
        ack = self.__ser.read(self.__wackLen) 
               
        #获取播放状态，直到设备播放停止
        stat = self.getPlayStat()
        while(stat != 0):
               stat = self.getPlayStat()                          
               
        return True
        
    #######################################
    ##    get play status
    ##    0(停止)1(播放) 2(暂停) 3(快进)4(快退)
    #######################################    
    def getPlayStat(self):
        list = [0x3]
        list.append(self.__cmd_reqDict['PlayStat'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        time.sleep(1)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False
        time.sleep(1)
        ack = self.__ser.read(self.__ackLen)
        self.__logger.info(ack)
        print ack
        if ack.find('OK0000') != -1:
                return 0
        elif ack.find('OK0001') != -1:
                return 1
        elif ack.find('OK0002') != -1:
                return 2
        elif ack.find('OK0003') != -1:
                return 3
        elif ack.find('OK0004') != -1:
                return 4
        else:
                return 5

    #######################################
    ##    get play volume
    #######################################    
    def getVolume(self):
        list = [0x3]
        list.append(self.__cmd_reqDict['Volume'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        time.sleep(1)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False
        ack = self.__ser.read(self.__ackLen)
        self.__logger.info(ack)
        if ack.find('OK') == -1:
           return False
        valueStr = '0x' + ack[2:]
        value = string.atoi(valueStr, 16) 
                 
        return value      

    #######################################
    ##    get current play device
    ##    0:USB 2:SPI
    #######################################    
    def getPlayDev(self):
        list = [0x3]
        list.append(self.__cmd_reqDict['PlayDev'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        time.sleep(1)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False
        ack = self.__ser.read(self.__ackLen)
        self.__logger.info(ack)
        if ack.find('OK') == -1:
           return False
        valueStr = '0x' + ack[2:]
        value = string.atoi(valueStr, 16) 
                 
        return value                

    #######################################
    ##    get current music index in Flash
    ##    1-255
    #######################################    
    def getMusicInFlash(self):
        list = [0x3]
        list.append(self.__cmd_reqDict['MusicInFlash'])
        cmd = self.__makeCommand(list)

        length = self.__ser.write(cmd)
        time.sleep(1)
        if length != len(cmd):
               self.__logger.info('write %d - %d /dev/ttyS2 failed.', len, len(cmd))
               return False
        ack = self.__ser.read(self.__ackLen)
        self.__logger.info(ack)
        if ack.find('OK') == -1:
           return False
        valueStr = '0x' + ack[2:]
        value = string.atoi(valueStr, 16) 
                 
        return value        
        
        
                                                             
