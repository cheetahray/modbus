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

def click(X, Y):
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
        di8 = (holdingRegisters[0] & 0x0080)
        #di9 = (holdingRegisters[0] & 0x0100) >> 8
        #di10 = (holdingRegisters[0] & 0x0200) >> 9
        if(di8 == 0):
            click(unit,pos[unit])
            '''
            holdingRegisters = modbusClient.ReadHoldingRegisters(0x0024, 2, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
            #print (holdingRegisters)
            pos[unit] = (holdingRegisters[1] << 16) + holdingRegisters[0]
            print (pos[unit])
            '''
    else:
        pass
        #print (ii)

def goZero(unit):
    
    modbusClient.UnitIdentifier = unit
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0703, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    #modbusClient.WriteMultipleRegisters(0x0700, [0x0002, 0x0000], unit)
    #modbusClient.WriteMultipleRegisters(0x0702, [0, 0], unit)
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0706, 2, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    modbusClient.WriteSingleRegister(0x0840, 25, unit)
    modbusClient.WriteMultipleRegisters(0x0704, [0x0012, 0x0000], unit)
    modbusClient.WriteSingleRegister(0x08A2, 0, unit)
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x08A2, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
        
def moveMotor(unit, howmany, speed):

    modbusClient.UnitIdentifier = unit
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0703, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    '''
    if 1 == speed:
        speed = 2
    elif 2 == speed:
        speed = 1
    if speed <= 7 and speed >= 1:
        speed = speed - 1            
        modbusClient.WriteSingleRegister(0x0705, speed, unit) #modbusClient.WriteMultipleRegisters(0x0704, [0x0012, speed], unit)
    '''
    if 1 > speed:
        speed = 1
    elif 1000 < speed:
        speed = 1000
    modbusClient.WriteSingleRegister(0x0840, speed, unit)
    #print artdmx[howmany]
    modbusClient.WriteMultipleRegisters(0x0706, [artdmx[howmany-1] & 0xFFFF, artdmx[howmany-1] >> 16], unit)
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x0706, 2, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    modbusClient.WriteSingleRegister(0x08A2, 1, unit)
    #holdingRegisters = modbusClient.ReadHoldingRegisters(0x08A2, 1, unit) #holdingRegisters = ConvertRegistersToFloat(modbusClient.ReadHoldingRegisters(2304, 1))
    #print (holdingRegisters)
    
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
        pos[unit] = (holdingRegisters[1] << 16) + holdingRegisters[0]
        print (pos[unit])
    
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
    #print (args[0], args[1], args[2]) 
    global func_list
    func_list.append( lambda : moveMotor( int(args[0]), int(args[1]), int(args[2]) ) )
	
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
cc.connect(('192.168.11.102', 4808))

modbusClient = ModbusClient('COM5') #modbusClient = ModbusClient('127.0.0.1', 502)
#modbusClient.Parity = Parity.odd
modbusClient.Parity = Parity.even
modbusClient.UnitIdentifier = 1
modbusClient.Baudrate = 115200
modbusClient.Stopbits = Stopbits.one
modbusClient.timeout = 0.016
modbusClient.Connect()
motornum = 25
pos = [0] * motornum
howmanylevel = 128
artdmx = [0] * howmanylevel
dividee = (100000000/howmanylevel)
    
for ii in range(0,howmanylevel):
    artdmx[ii] = int(ii * dividee * -1)
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
thread.start_new_thread(each_frame,())

func_list = []

for jj in range(0, motornum):
    goZero(jj+1)
                
while True:
    for jj in func_list:
        jj()
        func_list.pop(0)
    for ii in range(0, motornum):
        readInput(ii+1)
        #time.sleep(modbusClient.timeout)
		
modbusClient.close()
sock.close()
server.close()