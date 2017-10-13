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

def click(msg):
    global cc
    tracknum = "34"
    oscmsg = OSC.OSCMessage()
    oscstr = "%s" % ("/track" + tracknum + "/connect") 
    print (oscstr)
    oscmsg.setAddress(oscstr)
    oscmsg.append(1)
    cc.send(oscmsg)
    
def readInput(unit):
    modbusClient.UnitIdentifier = unit
    holdingRegisters = modbusClient.ReadHoldingRegisters(0x0204, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    if(len(holdingRegisters)):
        di9 = (holdingRegisters[0] & 0x0100) >> 8
        di10 = (holdingRegisters[0] & 0x0200) >> 9
        if(di9 > 0 or di10 > 0):
            print (di9, di10)
            #click(1)
    else:
        pass #print (ii)
        
def moveMotor(unit, howmany):
    '''
    discreteInputs = modbusClient.ReadDiscreteInputs(0, 8)
    print (discreteInputs)
    '''
    modbusClient.UnitIdentifier = unit
    holdingRegisters = modbusClient.ReadHoldingRegisters(0x0900, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
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
    if holdingRegisters[0] == 0x0ff0:
        '''
        modbusClient.WriteSingleRegister(2305, 3)
        modbusClient.WriteSingleRegister(2306, 200)
        modbusClient.WriteSingleRegister(2307, 300)
        modbusClient.WriteSingleRegister(2308, 2)
        time.sleep(2)
        modbusClient.WriteSingleRegister(2308, 0)
        modbusClient.WriteSingleRegister(2304, 0)
        '''
        #modbusClient.WriteSingleRegister(0x0901, 0, unit)
        
        modbusClient.WriteSingleRegister(0x0901, 4, unit)
        modbusClient.WriteSingleRegister(0x0902, 1000, unit)
        modbusClient.WriteSingleRegister(0x0903, 200, unit)
        #print ("{:04x}".format(abs(howmany)&0xFFFF))
        modbusClient.WriteSingleRegister(0x0905, abs(howmany) & 0xFFFF, unit)
        #print ("{:04x}".format(abs(howmany) >> 16))
        modbusClient.WriteSingleRegister(0x0906, abs(howmany) >> 16, unit)
        if(howmany > 0):
            modbusClient.WriteSingleRegister(0x0907, 1, unit)
        else:
            modbusClient.WriteSingleRegister(0x0907, 2, unit)
        #modbusClient.WriteSingleRegister(0x0901, 0)
        holdingRegisters = modbusClient.ReadHoldingRegisters(0x0024, 2, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
        #print (holdingRegisters)
        pos[unit] = (holdingRegisters[1] << 16) + holdingRegisters[0]
        print (pos[unit])
    
    else:
        print ("something wrong")
    '''
    modbusClient.WriteMultipleCoils(0, [True,True,True,True,True,False,True])
    modbusClient.WriteMultipleRegisters(0, ConvertFloatToTwoRegisters(3.141517))
    '''

def handler(socket,fortuple):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if ((len(data) > 18) and (data[0:8] == "Art-Net\x00")):
                rawbytes = map(ord, data)
                opcode = rawbytes[8] + (rawbytes[9] << 8)
                protocolVersion = (rawbytes[10] << 8) + rawbytes[11]
                if ((opcode == 0x5000) and (protocolVersion >= 14)):
                    sequence = rawbytes[12]
                    physical = rawbytes[13]
                    sub_net = (rawbytes[14] & 0xF0) >> 4
                    universe = rawbytes[14] & 0x0F
                    net = rawbytes[15]
                    rgb_length = (rawbytes[16] << 8) + rawbytes[17]
                    #print "seq %d phy %d sub_net %d uni %d net %d len %d" % \
                    #(sequence, physical, sub_net, universe, net, rgb_length)
                    idx = 18
                    x = 0
                    y = 0
                    while ((idx < (rgb_length+18)) and (y < 1)):
                        r = rawbytes[idx]
                        idx += 1
                        g = rawbytes[idx]
                        idx += 1
                        b = rawbytes[idx]
                        idx += 1
                        print "x %d y %d r %d g %d b %d" % (x,y,r,g,b)
                        #unicorn.set_pixel(x, y, r, g, b)
                        x += 1
                        if (x > 24):
                            x = 0
                            y += 1
            
        except ValueError:
            pass    
        except IndexError:
            pass
    
def user_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    # user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    print ("Now do something with", args[0]) 

# user script that's called by the game engine every frame
def each_frame():
    # simulate a "game engine"
    while True:
        # clear timed_out flag
        server.timed_out = False
        # handle all pending requests then return
        if not server.timed_out:
            server.handle_request()

cc = OSC.OSCClient()
cc.connect(('127.0.0.1', 6666))

modbusClient = ModbusClient('COM31') #modbusClient = ModbusClient('127.0.0.1', 502)
#modbusClient.Parity = Parity.odd
modbusClient.Parity = Parity.even
modbusClient.UnitIdentifier = 1
modbusClient.Baudrate = 115200
modbusClient.Stopbits = Stopbits.one
modbusClient.Connect()

pos = [0] * 25
artdmx = [0] * 256

dividee = (950000000/256)
    
for ii in range(0,256):
    artdmx[ii] = int(ii * dividee)
    print (artdmx[ii])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind(("0.0.0.0", 6454))

server = OSC.OSCServer( ("localhost", 7110) )
server.timeout = 0.001

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
server.handle_timeout = types.MethodType(handle_timeout, server)

server.addMsgHandler( "/user/1", user_callback )

#thread.start_new_thread(handler,(sock,0))
thread.start_new_thread(each_frame,())
    
while True:
    '''
    for ii in range(1,33):
        readInput(ii)
    '''
    moveMotor(1, 100000)
    time.sleep(1)

modbusClient.close()
sock.close()
server.close()