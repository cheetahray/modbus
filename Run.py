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
import random
import threading
import argparse

IN = [False, False, False, False, False, False]
def sec(idx,idx2):
    IN[idx] = False

def click(X, Y):
    global cc
    XX = X-1
    if(False == IN[XX]):
        threading.Timer(1, sec, (XX, XX)).start()
        oscmsg = OSC.OSCMessage()
        oscstr = "/Get"
        oscmsg.setAddress(oscstr)
        #oscstr = "%s %d %d" % (oscstr, X, count) 
        oscmsg.append(X-1)
        oscmsg.append(Y)
        print oscmsg
        cc.send(oscmsg)
        IN[XX] = True
    click2(X)

def click2(num):
    global dd
    oscmsg = OSC.OSCMessage()
    oscstr = "/Ballin"
    oscmsg.setAddress(oscstr)
    #oscstr = "%s %d %d" % (oscstr, X, count) 
    oscmsg.append(num)
    print oscmsg
    dd.send(oscmsg)
    
def readInput(unit):
    modbusClient.UnitIdentifier = unit
    holdingRegisters = modbusClient.ReadHoldingRegisters(0x0204, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    try:
        if(len(holdingRegisters)):
            #print (unit, holdingRegisters)
            #di8 = (holdingRegisters[0] & 0x0080)
            #di9 = (holdingRegisters[0] & 0x0100) >> 8
            #di10 = (holdingRegisters[0] & 0x0200) >> 9
            if(833 == holdingRegisters[0]):
                holdingRegisters = modbusClient.ReadHoldingRegisters(0x0024, 2, holdingRegisters[1]) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
                pos = artdmx[0] - (holdingRegisters[1] << 16) + holdingRegisters[0]
                print pos
                if False: #5 == unit:
                    click( holdingRegisters[2], math.ceil( float(pos) / artdmx2[0] * 127 ) )
                else:
                    click( holdingRegisters[2], math.ceil( float(pos) / artdmx[0] * 127 ) )
        else:
            #pass
            print (unit)
    except IndexError, e:
        pass
    
def goZero(unit,z1,z2):
    modbusClient.UnitIdentifier = unit
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0703, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    #modbusClient.WriteMultipleRegisters(0x0700, [0x0002, 0x0000], unit)
    #modbusClient.WriteMultipleRegisters(0x0702, [0, 0], unit)
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0706, 2, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    if "T" == z1:    
        modbusClient.WriteSingleRegister(0x0842, 250, unit)
        modbusClient.WriteSingleRegister(0x0862, 21000, unit)
        modbusClient.WriteSingleRegister(0x0844, 300, unit)
        modbusClient.WriteSingleRegister(0x0864, 10000, unit)
        modbusClient.WriteSingleRegister(0x0846, 600, unit)
        modbusClient.WriteSingleRegister(0x0866, 7000, unit)
        modbusClient.WriteSingleRegister(0x0848, 750, unit)
        modbusClient.WriteSingleRegister(0x0868, 6000, unit)
        modbusClient.WriteSingleRegister(0x084A, 900, unit)
        modbusClient.WriteSingleRegister(0x086A, 3750, unit)    
        motordistance = artdmx[127]
        modbusClient.WriteMultipleRegisters(0x0704, [0x1112, 0x0001], unit)
        modbusClient.WriteMultipleRegisters(0x0706, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0708, [0x2212, 0x0002], unit)
        modbusClient.WriteMultipleRegisters(0x070A, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x070C, [0x3312, 0x0003], unit)
        modbusClient.WriteMultipleRegisters(0x070E, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0710, [0x4412, 0x0004], unit)
        modbusClient.WriteMultipleRegisters(0x0712, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0714, [0x5512, 0x0005], unit)
        modbusClient.WriteMultipleRegisters(0x0716, [motordistance & 0xFFFF, motordistance >> 16], unit)
        motordistance = artdmx[100]
        modbusClient.WriteMultipleRegisters(0x0718, [0x1112, 0x0001], unit)
        modbusClient.WriteMultipleRegisters(0x071A, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x071C, [0x2212, 0x0002], unit)
        modbusClient.WriteMultipleRegisters(0x071E, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0720, [0x3312, 0x0003], unit)
        modbusClient.WriteMultipleRegisters(0x0722, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0724, [0x4412, 0x0004], unit)
        modbusClient.WriteMultipleRegisters(0x0726, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0728, [0x5512, 0x0005], unit)
        modbusClient.WriteMultipleRegisters(0x072A, [motordistance & 0xFFFF, motordistance >> 16], unit)
        motordistance = artdmx[75]
        modbusClient.WriteMultipleRegisters(0x072C, [0x1112, 0x0001], unit)
        modbusClient.WriteMultipleRegisters(0x072E, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0730, [0x2212, 0x0002], unit)
        modbusClient.WriteMultipleRegisters(0x0732, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0734, [0x3312, 0x0003], unit)
        modbusClient.WriteMultipleRegisters(0x0736, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0738, [0x4412, 0x0004], unit)
        modbusClient.WriteMultipleRegisters(0x073A, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x073C, [0x5512, 0x0005], unit)
        modbusClient.WriteMultipleRegisters(0x073E, [motordistance & 0xFFFF, motordistance >> 16], unit)
        motordistance = artdmx[50]
        modbusClient.WriteMultipleRegisters(0x0740, [0x1112, 0x0001], unit)
        modbusClient.WriteMultipleRegisters(0x0742, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0744, [0x2212, 0x0002], unit)
        modbusClient.WriteMultipleRegisters(0x0746, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0748, [0x3312, 0x0003], unit)
        modbusClient.WriteMultipleRegisters(0x074A, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x074C, [0x4412, 0x0004], unit)
        modbusClient.WriteMultipleRegisters(0x074E, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0750, [0x5512, 0x0005], unit)
        modbusClient.WriteMultipleRegisters(0x0752, [motordistance & 0xFFFF, motordistance >> 16], unit)
        motordistance = artdmx[25]
        modbusClient.WriteMultipleRegisters(0x0754, [0x1112, 0x0001], unit)
        modbusClient.WriteMultipleRegisters(0x0756, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0758, [0x2212, 0x0002], unit)
        modbusClient.WriteMultipleRegisters(0x075A, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x075C, [0x3312, 0x0003], unit)
        modbusClient.WriteMultipleRegisters(0x075E, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0760, [0x4412, 0x0004], unit)
        modbusClient.WriteMultipleRegisters(0x0762, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0764, [0x5512, 0x0005], unit)
        modbusClient.WriteMultipleRegisters(0x0766, [motordistance & 0xFFFF, motordistance >> 16], unit)
        motordistance = artdmx[0]
        modbusClient.WriteMultipleRegisters(0x0768, [0x1112, 0x0001], unit)
        modbusClient.WriteMultipleRegisters(0x076A, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x076C, [0x2212, 0x0002], unit)
        modbusClient.WriteMultipleRegisters(0x076E, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0770, [0x3312, 0x0003], unit)
        modbusClient.WriteMultipleRegisters(0x0772, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0774, [0x4412, 0x0004], unit)
        modbusClient.WriteMultipleRegisters(0x0776, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteMultipleRegisters(0x0778, [0x5512, 0x0005], unit)
        modbusClient.WriteMultipleRegisters(0x077A, [motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteSingleRegister(0x0840, 25, unit)
        modbusClient.WriteSingleRegister(0x0306, 33, unit)
        modbusClient.WriteSingleRegister(0x0700,  1, unit)
        modbusClient.WriteSingleRegister(0x031C,300, unit)
        modbusClient.WriteSingleRegister(0x031E,1000, unit)
    if "T" == z2:
        modbusClient.WriteSingleRegister(0x032C, 1, unit)
        modbusClient.WriteSingleRegister(0x08A2, 0, unit)
        #holdingRegisters = modbusClient.ReadHoldingRegisters(0x08A2, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
        #print (holdingRegisters)
        #time.sleep(modbusClient.writeTimeout)
        modbusClient.readmore(32)

def stop_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    # user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    print "stop", args[0] 
    modbusClient.WriteSingleRegister(0x08A2, 1000, args[0])

def moveMotor(unit, howmany, speed, acc):
    modbusClient.UnitIdentifier = unit
    
    motordistance = 0
    if False: #5 == unit:
        motordistance = artdmx2[howmany]#-1000000
    else:
        motordistance = artdmx[howmany] #1000000
    #print motordistance
    
    
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0703, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    
    #print artdmx[howmany]
    #modbusClient.WriteMultipleRegisters(0x0706, [motordistance & 0xFFFF, motordistance >> 16], unit)
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0706, 2, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    if 127 == howmany:
        modbusClient.WriteSingleRegister(0x08A2, speed+1, unit)
    elif 100 == howmany:
        modbusClient.WriteSingleRegister(0x08A2, speed+6, unit)
    elif 75 == howmany:
        modbusClient.WriteSingleRegister(0x08A2, speed+11, unit)
    elif 50 == howmany:
        modbusClient.WriteSingleRegister(0x08A2, speed+16, unit)
    elif 25 == howmany:
        modbusClient.WriteSingleRegister(0x08A2, speed+21, unit)
    elif 0 == howmany:
        modbusClient.WriteSingleRegister(0x08A2, speed+26, unit)
    else:
        idx = speed + 1
        modbusClient.WriteMultipleRegisters(0x0838, [0x0012 + (idx << 8) + (idx << 12), idx, motordistance & 0xFFFF, motordistance >> 16], unit)
        modbusClient.WriteSingleRegister(0x08A2, 63, unit)
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x08A2, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    #time.sleep(modbusClient.writeTimeout)
    #modbusClient.readmore(32)
    
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
    #global func_list
    #func_list.append( lambda : moveMotor( args[0], args[1], args[2], args[3] ) )
    moveMotor( args[0], args[1], args[2], args[3] )
    
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
dd.connect(('127.0.0.1', 7740))

modbusClient = ModbusClient('COM5') #modbusClient = ModbusClient('127.0.0.1', 502)
#modbusClient.Parity = Parity.odd
modbusClient.Parity = Parity.even
modbusClient.UnitIdentifier = 1
modbusClient.Baudrate = 115200
modbusClient.Stopbits = Stopbits.one
#modbusClient.timeout = 0.001
modbusClient.Connect()
motornum = 6
howmanylevel = 128
artdmx = [0] * howmanylevel
artdmx2 = [0] * howmanylevel
dividee = (100000000/howmanylevel)
dividee2 = (95900000/howmanylevel)    
for ii in range(0,howmanylevel):
    artdmx[howmanylevel-ii-1] = int(ii * dividee) + 300000
    artdmx2[howmanylevel-ii-1] = int(ii * dividee2) + 300000
for ii in range(0,howmanylevel):
    print (artdmx[ii])

#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#sock.bind(("0.0.0.0", 6454))

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
server.addMsgHandler( "/stop", stop_callback )

#thread.start_new_thread(handler,(sock,0))
_thread.start_new_thread(each_frame,())

func_list = []
fromwho = 1
towho = 7

parser = argparse.ArgumentParser()
parser.add_argument("--z1", default="T")
parser.add_argument("--z2", default="T")
args = parser.parse_args()
        
for jj in range(fromwho, towho):
    if jj != 3:
        goZero(jj,args.z1,args.z2)
    #pass
'''
for next in range(fromwho, towho):
    click ( next, random.randint(1,127) )
    time.sleep(1)
'''
while True:
    '''
    for jj in func_list:
        jj()
        #print len(func_list)
        func_list.pop(0)
    '''
    for ii in range(fromwho, towho):
        readInput(ii)
        #if len(func_list) > 0:
            #break

modbusClient.close()
sock.close()
server.close()