from ModbusClient import *
import time
import OSC
import _thread
import sys
import types
import math
import random
import argparse

modbusClient = ModbusClient('COM14') #modbusClient = ModbusClient('127.0.0.1', 502)
#modbusClient.Parity = Parity.odd
modbusClient.Parity = Parity.even
modbusClient.UnitIdentifier = 1
modbusClient.Baudrate = 115200
modbusClient.Stopbits = Stopbits.one
#modbusClient.timeout = 0.001
modbusClient.Connect()

#print modbusClient.ReadHoldingRegisters(0x08AA, 2, 8)
#print modbusClient.ReadHoldingRegisters(0x08AC, 2, 8)
# incremental absolute
#print modbusClient.ReadHoldingRegisters(0x0336, 1, 14)

# Clear zero
#modbusClient.WriteSingleRegister(0x0338, 1, 14)    
#print modbusClient.ReadHoldingRegisters(0x0338, 1, 14)

# Clear Alert
#print modbusClient.ReadHoldingRegisters(0x0524, 1, 15)
#modbusClient.WriteSingleRegister(0x0524, 1, 15)    

# Read Alert
print modbusClient.ReadHoldingRegisters(0x0100, 1, 11)
#print modbusClient.ReadHoldingRegisters(0x0100, 1, 23)
# Read Distance
#holdingRegisters = modbusClient.ReadHoldingRegisters(0x0024, 2, 11) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
#print holdingRegisters
#print ( (holdingRegisters[1] << 16) + holdingRegisters[0] )

# incremental absolute
#modbusClient.WriteSingleRegister(0x0300, 4096, 14)    
#print modbusClient.ReadHoldingRegisters(0x0300, 1, 14)

# baudrate
#modbusClient.WriteSingleRegister(0x052A, 87, 14)    
#print modbusClient.ReadHoldingRegisters(0x052A, 1, 14)

# Clear Zero not Move
#modbusClient.WriteSingleRegister(0x0306, 33, 14)    
#print modbusClient.ReadHoldingRegisters(0x0306, 1, 14)

# Go Zero
#modbusClient.WriteSingleRegister(0x08A2, 1000, 3)
#modbusClient.WriteSingleRegister(0x08A2, 1000, 12)
#modbusClient.WriteSingleRegister(0x08A2, 1000, 11)
#modbusClient.WriteSingleRegister(0x08A2, 1000, 10)
#modbusClient.WriteSingleRegister(0x08A2, 1000, 14)
# Write PR
#motordistance = 3937800000
#idx = 1
#modbusClient.WriteMultipleRegisters(0x0838, [0x0012 + (idx << 8) + (idx << 12), idx, motordistance & 0xFFFF, motordistance >> 16], 14)
#modbusClient.WriteSingleRegister(0x08A2, 63, 14)