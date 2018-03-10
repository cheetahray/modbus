#!/usr/bin/env python
'''
Created on 12.09.2016

@author: Stefan Rossmann
'''
from ModbusClient import *
import time
import OSC
import _thread
import sys
import types
import math
count = 0
def click(X, Y):
    global cc
    global count
    oscmsg = OSC.OSCMessage()
    oscstr = "/Get"
    oscmsg.setAddress(oscstr)
    #oscstr = "%s %d %d" % (oscstr, X, count) 
    oscmsg.append(X)
    oscmsg.append(Y)
    print oscmsg
    cc.send(oscmsg)
    count+=1
    click2()

def click2():
    global dd
    oscmsg = OSC.OSCMessage()
    oscstr = "/Ballin"
    oscmsg.setAddress(oscstr)
    #oscstr = "%s %d %d" % (oscstr, X, count) 
    oscmsg.append(1)
    print oscmsg
    dd.send(oscmsg)
    
def readInput(unit):
    modbusClient.UnitIdentifier = unit
    holdingRegisters = modbusClient.ReadHoldingRegisters(0x0204, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    try:
        if(len(holdingRegisters)):
            print (unit, holdingRegisters)
            #di8 = (holdingRegisters[0] & 0x0080)
            #di9 = (holdingRegisters[0] & 0x0100) >> 8
            #di10 = (holdingRegisters[0] & 0x0200) >> 9
            if(833 == holdingRegisters[0]):
                holdingRegisters = modbusClient.ReadHoldingRegisters(0x0024, 2, holdingRegisters[1]) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
                print (holdingRegisters)
                pos = (holdingRegisters[1] << 16) + holdingRegisters[0]
                click( holdingRegisters[2]-1, math.ceil( float(pos) / artdmx[0] * 127 ) )
        else:
            pass
            #print (unit)
    except IndexError, e:
        pass
	
def goZero(unit):
    modbusClient.UnitIdentifier = unit
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0703, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    #modbusClient.WriteMultipleRegisters(0x0700, [0x0002, 0x0000], unit)
    #modbusClient.WriteMultipleRegisters(0x0702, [0, 0], unit)
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0706, 2, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    modbusClient.WriteSingleRegister(0x032C, 1, unit)
    modbusClient.WriteSingleRegister(0x0840, 25, unit)
    modbusClient.WriteMultipleRegisters(0x0704, [0x0012, 0x0000], unit)
    modbusClient.WriteSingleRegister(0x08A2, 0, unit)
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x08A2, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    modbusClient.readmore(32)
    
def moveMotor(unit, howmany, speed, acc):
    modbusClient.UnitIdentifier = unit
    motordistance = 0
    if False: #unit == 25:
        motordistance = artdmx[howmany] * -1 #-1000000
    else:
        motordistance = artdmx[howmany] #1000000
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0703, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    #print motordistance
    '''
    if 1 == speed:
        speed = 2
    elif 2 == speed:
        speed = 1
    if speed <= 7 and speed >= 1:
        speed = speed - 1            
        modbusClient.WriteSingleRegister(0x0705, speed, unit) #modbusClient.WriteMultipleRegisters(0x0704, [0x0012, speed], unit)
    if 1 > speed:
        speed = 1
    elif 1000 < speed:
        speed = 1000
    '''
    modbusClient.WriteSingleRegister(0x0840, speed, unit)
    modbusClient.WriteSingleRegister(0x0860, acc, unit)
    #print artdmx[howmany]
    modbusClient.WriteMultipleRegisters(0x0706, [motordistance & 0xFFFF, motordistance >> 16], unit)
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0706, 2, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    modbusClient.WriteSingleRegister(0x08A2, 1, unit)
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x08A2, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    modbusClient.readmore(32)
    
def JogMotor(unit, JogWhat):
    
    modbusClient.UnitIdentifier = unit
    holdingRegisters = modbusClient.ReadHoldingRegisters(0x0900, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    print (holdingRegisters)

    if holdingRegisters[0] == 0x0ff0:
        #modbusClient.WriteSingleRegister(0x0901, 0, unit)
        
        modbusClient.WriteSingleRegister(0x0901, 3, unit)
        modbusClient.WriteSingleRegister(0x0902, 1000, unit)
        modbusClient.WriteSingleRegister(0x0903, 20, unit)
        #print ("{:04x}".format(abs(howmany) >> 16))
        modbusClient.WriteSingleRegister(0x0904, JogWhat, unit)
        holdingRegisters = modbusClient.ReadHoldingRegisters(0x0024, 2, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
        #print (holdingRegisters)
        
    else:
        print ("something wrong")

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
                        print ("x %d y %d r %d g %d b %d" % (x,y,r,g,b))
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
    print (args[0], args[1], args[2], args[3]) 
    global func_list
    func_list.append( lambda : moveMotor( args[0], args[1], args[2], args[3] ) )
    
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
cc.connect(('127.0.0.1', 7110))
dd = OSC.OSCClient()
dd.connect(('192.168.1.108', 7740))

modbusClient = ModbusClient('COM37') #modbusClient = ModbusClient('127.0.0.1', 502)
#modbusClient.Parity = Parity.odd
modbusClient.Parity = Parity.even
modbusClient.UnitIdentifier = 1
modbusClient.Baudrate = 115200
modbusClient.Stopbits = Stopbits.one
#modbusClient.timeout = 0.001
modbusClient.Connect()
motornum = 13
howmanylevel = 128
artdmx = [0] * howmanylevel
dividee = (100000000/howmanylevel)
    
for ii in range(0,howmanylevel):
    artdmx[howmanylevel-ii-1] = int(ii * dividee)

for ii in range(0,howmanylevel):
    print (artdmx[ii])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind(("0.0.0.0", 6454))

server = OSC.OSCServer( ("0.0.0.0", 7730) )
server.timeout = 0.001

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
server.handle_timeout = types.MethodType(handle_timeout, server)

server.addMsgHandler( "/motor", user_callback )

#thread.start_new_thread(handler,(sock,0))
_thread.start_new_thread(each_frame,())

func_list = []
#for jj in range(1, motornum):
#for jj in range(motornum, 25):
for jj in range(1, 2):
    goZero(jj)

while True:
    for jj in func_list:
        jj()
        #print len(func_list)
        func_list.pop(0)
    for ii in range(1, motornum):
    #for ii in range(motornum, 25):
        readInput(ii)
        if len(func_list) > 0:
            break
        
modbusClient.close()
sock.close()
server.close()