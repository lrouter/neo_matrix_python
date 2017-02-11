#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import serial
import logging
import re
import matrix_usrwifi as muw
import matrix_net as mnt
import matrix_logger as mlog

class NetMonitor:
    def __init__(self): 
        # 创建一个logger
        # 创建一个handler，用于写入日志文件
        self.__logger =  mlog.MatrixLogger('NetMonitor.log')
       
        #######################################################################################
        #设置USR WIFI 模块处于TCP服务器模式,STA,保存为默认参数
        #######################################################################################
        self.__logger.info("设置USR WIFI 模块处于TCP服务器模式")
        self.__uwifi = muw.UsrWifi()
        self.__uwifi.init()
        time.sleep(0.5) #wait for 0.5 second

    def monitor(self):    
        #######################################################################################
        #监控USR WIFI模块的输出
        #######################################################################################
        while True:
              #获取LAN和WAN的连接状态
              self.__logger.info('获取LAN和WAN的连接状态')
              net = mnt.Net()
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
      
      
      
      
            
           
          
             
            
            




    





        
