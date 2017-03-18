#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import serial
import logging
import re
import neo_matrix_python as ma

class NetMonitor:
    def __init__(self): 
        # Creat log
        self.__logger = ma.MatrixLogger("NetMonitor.log")
        
        # Creat led inode
        self.__logger.info("Creat led inode in file system")
        
        # 记录一条日志
        self.__logger.info('first message.')
        
        #######################################################################################
        #设置USR WIFI 模块处于TCP服务器模式,STA,保存为默认参数
        #######################################################################################
        self.__logger.info("设置USR WIFI 模块处于TCP服务器模式")
        self.__uwifi = ma.UsrWifi()
        self.__uwifi.init()
        time.sleep(0.5) #wait for 0.5 second

    def monitor(self):    
        #######################################################################################
        #监控USR WIFI模块的输出
        #######################################################################################
        while True:
              #获取LAN和WAN的连接状态
              self.__logger.info('获取LAN和WAN的连接状态')
              net = ma.Net()
              lanstat = net.isLanLink()
              wanstat = net.isWanLink()
              self.__logger.info('lanstat = %d', lanstat)
              self.__logger.info('wanstat = %d', wanstat)
              
              #更新文件中保存的LAN和WAN的连接状态
              
              #检查串口是否有数据
              self.__logger.info('检查串口是否有数据')
              data = self.__uwifi.rxData()
              while cmp(data, '') == 0:
                 data = self.__uwifi.rxData()
                 
              self.__logger.info('data = %s', data)
              
              #从串口数据中解析出wifi名称和密码
              self.__logger.info('从串口数据中解析出wifi名称和密码')
              pdata = data.splitlines()
              if cmp(pdata[0], "start") == 0 and cmp(pdata[4], "end") == 0:
                  wifi_name = pdata[1]
                  wifi_passwd = pdata[2]
                  self.__logger.info('wifi_name = %s', wifi_name)
                  self.__logger.info('wifi_passwd = %s', wifi_passwd)
              else:
                   continue
              
              #使用解析出的wifi名称和密码，更新板载wifi配置文件
              self.__logger.info('更新板载wifi配置文件')
              wifi_config_file = "/etc/wpa_supplicant/wpa_supplicant.conf"
              os.system('cp /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.back')
              
              alllines = ""
              f = open(wifi_config_file,'r')
              line = f.readline()
              while line:
                    if line.find("ssid=") != -1:
                       line = "\tssid=" + "\"" +  wifi_name + "\"" + "\n"
                    elif line.find("psk=") != -1:
                       line = "\tpsk=" + "\"" +  wifi_passwd + "\"" + "\n"
                    alllines = alllines + line
                    line = f.readline()
              f.close()
              
              f=open(wifi_config_file,'w+')    
              f.writelines(alllines)  
              f.close()
              
              #使板载wifi重新连接
              self.__logger.info('使板载wifi重新连接')
              os.system("ifdown wlan0")
              os.system("ifup wlan0")
              time.sleep(1)
      
      
      
      
            
           
          
             
            
            




    





        
