#!/usr/bin/python
# -*- coding: UTF-8 -*-
from OSC import *
import sys
from time import sleep
import random
import socket
import thread
import json
import requests
import urllib
import threading
import datetime
from expy.excel import Excel
#          1                   2                  3                 4                   5
XY=[[-2960,[100,-100]],[-2900,[160,-160]],[-2840,[180,-180]],[-2730,[180,-180]],[-2700,[180,-180]], #1
    [-2600,[180,-180]],[-2565,[180,-180]],[-2460,[180,-180]],[-2430,[180,-180]],[-2325,[180,-180]], #2
    [-2295,[180,-180]],[-2190,[180,-180]],[-2160,[180,-180]],[-2050,[180,-180]],[-2025,[180,-180]], #3
    [-1915,[180,-180]],[-1885,[180,-180]],[-1780,[180,-180]],[-1750,[180,-180]],[-1645,[180,-180]], #4
    [-1615,[180,-180]],[-1510,[180,-180]],[-1480,[180,-180]],[-1370,[180,-180]],[-1345,[180,-180]], #5
    [-1240,[180,-180]],[-1175,[160,-160]],[-1120,[100,-100]],[-995 ,[100,-100]],[-935 ,[160,-160]], #6
    [-875 ,[180,-180]],[-815 ,[180,-180]],[-755 ,[160,-160]],[-695 ,[100,-100]],[-575 ,[100,-100]], #7
    [-515 ,[160,-160]],[-450 ,[180,-180]],[-390 ,[180,-180]],[-330 ,[160,-160]],[-270 ,[100,-100]], #8
    [-150 ,[100,-100]],[-90  ,[160,-160]],[-30  ,[180,-180]],[ 30  ,[180,-180]],[ 90  ,[160,-160]], #9
    [ 150 ,[100,-100]],[ 270 ,[100,-100]],[ 330 ,[160,-160]],[ 390 ,[180,-180]],[ 450 ,[180,-180]],#10
    [ 515 ,[160,-160]],[ 575 ,[100,-100]],[ 695 ,[100,-100]],[ 755 ,[160,-160]],[ 815 ,[180,-180]],#11
    [ 875 ,[180,-180]],[ 935 ,[160,-160]],[ 995 ,[100,-100]],[ 1120,[100,-100]],[ 1175,[160,-160]],#12
    [ 1240,[180,-180]],[ 1345,[180,-180]],[ 1370,[180,-180]],[ 1480,[180,-180]],[ 1510,[180,-180]],#13
    [ 1615,[180,-180]],[ 1645,[180,-180]],[ 1750,[180,-180]],[ 1780,[180,-180]],[ 1885,[180,-180]],#14
    [ 1915,[180,-180]],[ 2025,[180,-180]],[ 2050,[180,-180]],[ 2160,[180,-180]],[ 2190,[180,-180]],#15
    [ 2295,[180,-180]],[ 2325,[180,-180]],[ 2430,[180,-180]],[ 2460,[180,-180]],[ 2565,[180,-180]],#16
    [ 2600,[180,-180]],[ 2700,[180,-180]],[ 2730,[180,-180]],[ 2840,[180,-180]],[ 2900,[160,-160]],#17
    [ 2960,[100,-100]]]
smallLen = XY[0][1][0] - XY[0][1][1]
smallTop = XY[0][1][0]
midLen = XY[1][1][0] - XY[1][1][1]
midTop = XY[1][1][0]
bigLen = XY[2][1][0] - XY[2][1][1]
bigTop = XY[2][1][0]
smallReal = 1281
midReal = 1860
bigReal = 2109
  
cc = OSCClient()
cc.connect(('192.168.1.200', 6666))   # localhost, port 57120
dd = OSCClient()
dd.connect(('192.168.1.202', 6662))   # localhost, port 57120
ee = OSCClient()
ee.connect(('127.0.0.1', 7730))   # localhost, port 57120
ff = OSCClient()
ff.connect(('127.0.0.1', 7731))   # localhost, port 57120
gg = OSCClient()
gg.connect(('127.0.0.1', 7732))   # localhost, port 57120
hh = OSCClient()
hh.connect(('127.0.0.1', 7733))   # localhost, port 57120
ll = OSCClient()
ll.connect(('127.0.0.1', 7111))   # localhost, port 57120

def whiteglove(arg0, oscmsg):
    global ee,ff,gg,hh
    wrong = []        
    try:
        if wrong.index(arg0) >= 0:
            pass
    except ValueError:
        if 1 <= arg0 and arg0 <= 6:
            ee.send(oscmsg)
        elif 7 <= arg0 and arg0 <= 12:
            ff.send(oscmsg)
        elif 13 <= arg0 and arg0 <= 18:
            gg.send(oscmsg)
        elif 19 <= arg0 and arg0 <= 24:
            hh.send(oscmsg)

def motor(msg,arg0,arg1,arg2,arg3):
    global close
    oscmsg = OSCMessage()
    oscmsg.setAddress(msg)
    oscmsg.append(arg0)
    if True:#datetime.datetime.now() < close:           
        oscmsg.append(arg1)
    else: 
        oscmsg.append(0) 
    oscmsg.append(arg2)
    oscmsg.append(arg3)
    #print oscmsg
    whiteglove(arg0, oscmsg)

def over(msg,arg0,arg1,arg2):
    global dd
    oscmsg = OSCMessage()
    oscmsg.setAddress(msg)
    oscmsg.append(arg0)
    oscmsg.append(arg1)
    oscmsg.append(arg2)
    print oscmsg
    dd.send(oscmsg)

def click(msg,arg0,arg1):
    global cc
    #if arg0==-270:
    #    print('get 40')
    #    return
    #print('[0]:{} [1]:{}'.format(arg0,arg1))
    oscmsg = OSCMessage()
    oscmsg.setAddress(msg)
    oscmsg.append(arg0)
    oscmsg.append(arg1)
    #print oscmsg
    cc.send(oscmsg)

def stop(msg,arg0):
    oscmsg = OSCMessage()
    oscmsg.setAddress(msg)
    oscmsg.append(arg0)
    whiteglove(arg0, oscmsg)
    
server = OSCServer( ("0.0.0.0", 7110) )
server.timeout = 0
run = True

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
server.handle_timeout = types.MethodType(handle_timeout, server)

TOUCHDOWN = 1
TOUCHRELEASE = 0
touchmode = [
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
		    ]

def release(args0, args00):
    global TOUCHRELEASE
    touchmode[args0] = TOUCHRELEASE            

def hit_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    # user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    global TOUCHDOWN, TOUCHRELEASE
    if touchmode[args[0]-1] == TOUCHRELEASE:
        args0 = args[0]-1
        args1 = args[1] * 10
        if args[0] > 86:
            print (path, args[0], args[1])
        elif XY[args0][1][1] == -180:
            print (path, args[0], args[1])
            click (path, XY[args0][0], bigTop - (bigLen * args1 / bigReal ))
        elif XY[args0][1][1] == -160:
            if False == specialII.has_key(args[0]) or args[1] < specialII.get(args[0]) :
                print (path, args[0], args[1])
                click (path, XY[args0][0], midTop - (midLen * args1 / midReal )) 
        elif XY[args0][1][1] == -100: 
            if False == special.has_key(args[0]) or args[1] < special.get(args[0]) :
                print (path, args[0], args[1])
                click (path, XY[args0][0], smallTop - (smallLen * args1 / smallReal ))
        touchmode[args0] = TOUCHDOWN
        threading.Timer(0.5, release, (args0,args0) ).start()
        
def get_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    # user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    #/BallIn
    print (path, args[0], args[1])
    click (path, args[0], ( ( 260 * int(args[1]) )  >> 7 ) - 100 )  #260 * Y / 128 - 100  

def crm(url2, myDict):
    url = 'http://183.131.3.182:9002/query.ashx?method=' #'http://47.97.194.91:8686/query.ashx?method='
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}     
    res = requests.post(url+url2, data= 'data=' + urllib.quote(json.dumps(myDict)), headers=headers)
    return json.loads(res.text)#.get('Data')
    
def ID_callback(path, tags, args, source):
    global sock,url
    # don't do this at home (or it'll quit blender)
    #global run
    #run = False
    global now
    
    global NowMode
    global sheetrow
    print (path, args[0])
    now = datetime.datetime.now()
    if 100 != NowMode and now.minute % 30 >= 24 :
        over ("/error", "d", "d", "d")
    else:    
        value = crm("PlayGames", {"VIPCODE": args[0]})
        if value.get('Data') == "B":
            print "Not member yet."   #憒?甇斗??⊿?瘝酉??? /error 0or1or2...
            over ("/error", "b", "b", "b")
        elif value.get('Data') == "C":
            print "Just in your game."
            over ("/error", "c", "c", "c")
        elif isinstance(value.get('Data'), dict):
            print value
            value2 = crm("GetGames", {"phone": value.get('Data').get('M_ID')})
            if value2.get('Data') == value.get('Data').get('M_ID'):
                SHEETROWs[value.get('Data').get('M_ID')] = sheetrow
                excel.write(sheetrow, 1, value.get('Data').get('M_ID'))
                cpan = value.get('Data').get('C_PAN')
                print cpan[-1:]
                over ("/IDdata", value.get('Data').get('M_ID'), int(value.get('Data').get('C_ID')), int(cpan[-1:])) #phone number, role number, color num
                sock.sendto(value.get('Data').get('M_ID').encode('utf8') + "!@#" + value.get('Data').get('C_NAME').encode('utf8'),("192.168.1.202",5678))
                sock.sendto(value.get('Data').get('M_ID').encode('utf8') + "!@#" + value.get('Data').get('C_NAME').encode('utf8'),("192.168.1.200",8765))      
                G_SCO[value2.get('Data')] = value.get('Data').get('G_SCO')
                excel.write(sheetrow, 3, value.get('Data').get('G_SCO'))
                G_BALLS[value2.get('Data')] = value.get('Data').get('G_BALLS')
                excel.write(sheetrow, 2, value.get('Data').get('G_BALLS'))
                #TRANS_SCO = int(value.get('Data').get('TRANS_SCO'))
                LAST_LOGIN = value.get('Data').get('LAST_LOGIN')
                if None == value.get('Data').get('L_TIMES'):
                    L_TIMES[value2.get('Data')] = "0"
                else:
                    L_TIMES[value2.get('Data')] = value.get('Data').get('L_TIMES')
                XF_VIPCODE[value2.get('Data')] = value.get('Data').get('XF_VIPCODE')
                excel.write(sheetrow, 0, value.get('Data').get('XF_VIPCODE'))
                excel.write(sheetrow, 8, datetime.datetime.now())
                excel.save()
                sheetrow+=1
            else:
                print "lock error."
                over ("/error", "d", "d", "d")
        else: #elif value.get('Data')[0] == "A":
            #XF_VIPCODE = value.get('Data')[value.get('Data').index(":")+1:]
            print "Not opened card yet."     
            over ("/error", "a", "a", "a")        
        
def IDscore_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    #global run
    #run = False
    #add old data then restore back
    
    retupdate = 0
    print (path, args[0], args[1], args[2]) #?活蝮賢? ?活?脩???
    UPDATE = {"trans":{"XF_VIPCODE":XF_VIPCODE[args[0]],"M_ID":args[0],"G_SCO":int(G_SCO[args[0]])+int(args[1]),"G_BALLS":int(G_BALLS[args[0]])+int(args[2]),"L_TIMES":int(L_TIMES[args[0]])+1}}
    print UPDATE
    excel.write(SHEETROWs[args[0]], 4, args[2])
    excel.write(SHEETROWs[args[0]], 5, args[1])
    excel.write(SHEETROWs[args[0]], 6, UPDATE.get("trans").get('G_BALLS'))
    excel.write(SHEETROWs[args[0]], 7, UPDATE.get("trans").get('G_SCO'))
    excel.save()
    value = crm("GetGamesdes", {"phone": args[0]})
    if(value.get('Data') == args[0]):
        value = crm("translationUpdate",UPDATE)
        if value.get('Data') == args[0]:
            retupdate = 1

    over("/update", args[0], retupdate, retupdate) #憒?銝銝???/update 0

def user_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    # user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    #print (args[0], args[1], args[2], args[3]) 
    motor (path, args[0], args[1], args[2], args[3])

def stop_callback(path, tags, args, source):
    print (path, args[0]) 
    '''
    for next in range(args[0], args[1]+1):
        stop ("/stop", next)
        time.sleep(0.05)
    '''
    stop ("/stop", args[0])

def scene_callback(path, tags, args, source):
    global NowMode, fishcnt, ll
    # don't do this at home (or it'll quit blender)
    #global run
    #run = False
    #add old data then restore back
    print (path, args[0], args[1]) #tel 1/0
    if 2 == args[1]:
        NowMode = 100
    else:
        NowMode = args[0]
    print NowMode
    oscmsg = OSCMessage()
    oscmsg.setAddress(path)
    oscmsg.append(args[0])
    oscmsg.append(args[1])
    print oscmsg
    ll.send(oscmsg)
    #now = datetime.datetime.now()
    #print now.year, now.month, now.day, now.hour, now.minute, now.second

SHEETROWs = {}
excel = Excel( "C:\\Users\\goingdown\\Documents\\keil\\5YD-UDP\\data.xls", "sheet1", False)
sheet = excel.read()
sheetrow = sheet.nrows
	
server.addMsgHandler( "/Hit", hit_callback )
server.addMsgHandler( "/Get", get_callback )
server.addMsgHandler( "/ID", ID_callback )
server.addMsgHandler( "/IDscore", IDscore_callback )
server.addMsgHandler( "/motor", user_callback )
server.addMsgHandler( "/stop", stop_callback )
server.addMsgHandler( "/Scene", scene_callback )

# user script that's called by the game engine every frame
def each_frame():
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()

def handler(socket,fortuple):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.error, e:
            pass
special = {29:122, 34:117, 35:112, 40:137, 41:127, 46:110, 52:127, 53:120}
specialII = {30:15, 45:161, 57:168, 85:136}
G_SCO = {}
G_BALLS = {}
#TRANS_SCO = 0
L_TIMES = {}
XF_VIPCODE = {}
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#sock.bind(("0.0.0.0", 8756))
#_thread.start_new_thread(handler,(sock,0))
NowMode = 0
now = datetime.datetime.now()
close = datetime.datetime(now.year, now.month, now.day, 21, 3, 0)
'''
for ii in range (1,5):
    motor("/motor", ii, 0, 0, 0)
    sleep(0.5)
for ii in range (9,13):
    motor("/motor", ii, 0, 0, 0)
    sleep(0.5)
for ii in range (13,17):
    motor("/motor", ii, 0, 0, 0)
    sleep(0.5)
'''
'''
print sheet.nrows
print sheet.ncols
try:
    while len(sheet(sheetrow, 0)) > 0:
        sheetrow+=1
except IndexError:
    excel.write(sheetrow, 0, "Fa")
    excel.save()
'''
while True:
    each_frame()
    
for next in range(len(XY), len(XY)):
    click ("/Hit", XY[next][0], 180)
    time.sleep(2)

server.close()