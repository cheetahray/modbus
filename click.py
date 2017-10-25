import OSC
import time 

def click(unit, msg):
    global cc
    oscmsg = OSC.OSCMessage()
    oscstr = "%s" % ("/user/1") 
    print (oscstr)
    oscmsg.setAddress(oscstr)
    oscmsg.append(unit)
    oscmsg.append(msg)
    cc.send(oscmsg)

cc = OSC.OSCClient()
cc.connect(('127.0.0.1', 7110))

while True:
    click(1,1000000)
    time.sleep(1)
    click(1,-1000000)
    time.sleep(1)
    