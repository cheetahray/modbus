#!/usr/bin/env python
'''
Created on 12.09.2016

@author: Stefan Rossmann
'''
from ModbusClient import *
import time
    
modbusClient = ModbusClient('/dev/ttyS26') #modbusClient = ModbusClient('127.0.0.1', 502)
#modbusClient.Parity = Parity.odd
modbusClient.Parity = Parity.even
modbusClient.UnitIdentifier = 1
modbusClient.Baudrate = 9600
modbusClient.Stopbits = Stopbits.one
modbusClient.Connect()
'''
discreteInputs = modbusClient.ReadDiscreteInputs(0, 8)
print (discreteInputs)
'''

holdingRegisters = modbusClient.ReadHoldingRegisters(2304, 1) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
print (holdingRegisters)

'''
inputRegisters = modbusClient.ReadInputRegisters(2304, 1)
print (inputRegisters)
'''
'''
coils = modbusClient.ReadCoils(0, 8)
print (coils)
modbusClient.WriteSingleCoil(0, True)
'''
if holdingRegisters[0] == 4080:
    modbusClient.WriteSingleRegister(2305, 3)
    modbusClient.WriteSingleRegister(2306, 200)
    modbusClient.WriteSingleRegister(2307, 300)
    modbusClient.WriteSingleRegister(2308, 2)
    time.sleep(2)
    modbusClient.WriteSingleRegister(2308, 0)
    modbusClient.WriteSingleRegister(2304, 0)
else:
    print ("something wrong")
'''
modbusClient.WriteMultipleCoils(0, [True,True,True,True,True,False,True])
modbusClient.WriteMultipleRegisters(0, ConvertFloatToTwoRegisters(3.141517))
'''
modbusClient.close()