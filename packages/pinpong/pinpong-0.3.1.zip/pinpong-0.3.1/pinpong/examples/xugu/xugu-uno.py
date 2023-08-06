# -*- coding: utf-8 -*-

#实验效果：同时控制xugu版和UNO板的板载LED灯
#接线：将一个Uno通过USB口连接在虚谷上
'''
import time
from pinpong.board import Board,Pin

Board("xugu").begin()#先初始化，被认为是默认主板
uno = Board("uno").begin()

xugu_led = Pin(Pin.D13, Pin.OUT) #默认主板不需要输入board参数
uno_led = Pin(uno, Pin.D13, Pin.OUT)

while True:
  print("control xugu board")
  for i in range(3):
    xugu_led.value(1) #输出高电平
    time.sleep(1) #等待1秒 保持状态
    xugu_led.value(0) #输出低电平
    time.sleep(1) #等待1秒 保持状态

  print("control uno board")
  for i in range(3):
    uno_led.value(1) #输出高电平
    time.sleep(1) #等待1秒 保持状态
    uno_led.value(0) #输出低电平
    time.sleep(1) #等待1秒 保持状态
'''

import time
from pinpong.board import Board,Pin

xugu = Board("xugu").begin()
uno = Board("uno").begin()
Board.set_default_board(uno)#手动设置默认主板

xugu_led = Pin(xugu,Pin.D13, Pin.OUT) 
uno_led = Pin(Pin.D13, Pin.OUT) #默认主板不需要输入board参数

while True:
  print("control xugu board")
  for i in range(3):
    xugu_led.value(1) #输出高电平
    time.sleep(1) #等待1秒 保持状态
    xugu_led.value(0) #输出低电平
    time.sleep(1) #等待1秒 保持状态

  print("control uno board")
  for i in range(3):
    uno_led.value(1) #输出高电平
    time.sleep(1) #等待1秒 保持状态
    uno_led.value(0) #输出低电平
    time.sleep(1) #等待1秒 保持状态
