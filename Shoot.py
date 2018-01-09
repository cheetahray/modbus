#!/usr/bin/env python
'''
Created on 12.09.2016

@author: Stefan Rossmann
'''
from ModbusClient import *
import time
import OSC
import thread
import sys
import types

def click(msg, X, Y):
    global cc
    oscmsg = OSC.OSCMessage()
    oscstr = "/Get"
    oscmsg.setAddress(oscstr)
    oscstr = "%s %d %d" % (oscstr, X, Y) 
    print (oscstr)
    oscmsg.append(X)
    oscmsg.append(Y)
    cc.send(oscmsg)
    
def readInput(unit):
    modbusClient.UnitIdentifier = unit
    holdingRegisters = modbusClient.ReadHoldingRegisters(0x0204, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    if(len(holdingRegisters)):
        d8 = (holdingRegisters[0] & 0x0080)
        #di9 = (holdingRegisters[0] & 0x0100) >> 8
        #di10 = (holdingRegisters[0] & 0x0200) >> 9
        if(di8 == 0):
            #click(1)
            holdingRegisters = modbusClient.ReadHoldingRegisters(0x0024, 2, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
            #print (holdingRegisters)
            pos[unit] = (holdingRegisters[1] << 16) + holdingRegisters[0]
            print (pos[unit])
    else:
        print (ii)
        
cc = OSC.OSCClient()
cc.connect(('127.0.0.1', 6666))

modbusClient = ModbusClient('COM31') #modbusClient = ModbusClient('127.0.0.1', 502)
#modbusClient.Parity = Parity.odd
modbusClient.Parity = Parity.even
modbusClient.UnitIdentifier = 1
modbusClient.Baudrate = 115200
modbusClient.Stopbits = Stopbits.one
modbusClient.Connect()
motornum = 25
pos = [0] * motornum

while True:
    for ii in range(1,motornum):
        readInput(ii)
        time.sleep(0.016)
		
modbusClient.close()
sock.close()
server.close()