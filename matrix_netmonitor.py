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
        self.__logger = ma.MatrixLogger("NetMonitor")

        #######################################################################################
        # 设置USR WIFI 模块处于TCP服务器模式,STA,保存为默认参数
        #######################################################################################
        self.__uwifi = ma.UsrWifi()
        self.__uwifi.init()
        time.sleep(0.5)  # wait for 0.5 second

    def monitor(self):
        #######################################################################################
        # 监控USR WIFI模块的输出
        #######################################################################################
        while True:
            # 获取LAN和WAN的连接状态
            net = ma.Net()
            lanstat = net.isLanLink()
            wanstat = net.isWanLink()

            # 更新文件中保存的LAN和WAN的连接状态

            # 检查串口是否有数据
            data = self.__uwifi.rxData()
            while cmp(data, '') == 0:
                data = self.__uwifi.rxData()

            # 从串口数据中解析出wifi名称和密码
            pdata = data.splitlines()
            if cmp(pdata[0], "start") == 0 and cmp(pdata[4], "end") == 0:
                wifi_name = pdata[1]
                wifi_passwd = pdata[2]
                self.__logger.info('wifi_name = %s', wifi_name)
                self.__logger.info('wifi_passwd = %s', wifi_passwd)
            else:
                continue

            # 使用解析出的wifi名称和密码，重新连接wifi
            cmdstr = 'nmcli radio wifi on'
            os.system(cmdstr)
            cmdstr = 'nmcli device wifi rescan'
            os.system(cmdstr)
            cmdstr = 'nmcli dev wifi connect' + ' ' + wifi_name + ' ' + password + ' ' + wifi_passwd
            os.system(cmdstr)
