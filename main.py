#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
Our main file
'''
import qrcode, requests, pifacecad, os, socket

def print_instructions_rasperry():
    cad.lcd.clear()
    cad.lcd.set_cursor(0, 0)
    cad.lcd.write("0: read QR \n")
    cad.lcd.write("2: abort")
    
def print_instructions():
    print ("Switch 0: QR Code Scanning...")
    print ("Switch 2: abort")
 
def finish_aplication(event):
    cad.lcd.clear()
    cad.lcd.set_cursor(0, 0)
    cad.lcd.write("Closing the application...")
    print ("closing...")
    os.kill(os.getppid(),9)

def qr_reader(event):
    cad.lcd.clear()
    cad.lcd.set_cursor(0, 0)#
    global result
    result=qrcode.read().strip()
    print ("QR Code is" + result.decode('ascii')) #present in string format
    # p = requests.post("http://ats-1-7.appspot.com/AttendanceLog/123456/"+result.decode('ascii'))
    #print(p.text)
   # print (p.status_code, p.reason)
    print ("READER FINISHED")
   # cad.lcd.write(str(p.status_code))
    cad.lcd.write("\nQR DONE")
    print_present()
    
def presented(event):
    cad.lcd.clear()
    cad.lcd.set_cursor(0,0)
    t = "true"
    global postStringArray
    global result
    try: # try and catch block for the case of being offline
        p= requests.post("http://ats-1-7.appspot.com/AttendanceLog/123456/"+result.decode('ascii')+"/true/")
        print(p.text)
        cad.lcd.write(str(p.status_code))
    except requests.exceptions.RequestException as e:
        print ("A connection error occured")
        save_offline("http://ats-1-7.appspot.com/AttendanceLog/123456/"+result.decode('ascii')+"/true/")
        print(postStringArray)
        
    print ("FINISHED")
    cad.lcd.write("\nFINISHED")
    print_instructions()
    print_instructions_rasperry()  
            
def not_presented(event):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cad.lcd.clear()
    cad.lcd.set_cursor(0,0)
    global result
    try:
        p= requests.post("http://ats-1-7.appspot.com/AttendanceLog/123456/"+result.decode('ascii')+"/false/")
        print(p.text)
        cad.lcd.write(str(p.status_code))
    except requests.exceptions.RequestException as e:
        print ("A connection error occured")
        save_offline("http://ats-1-7.appspot.com/AttendanceLog/123456/"+result.decode('ascii')+"/false/")
        print(postStringArray)  
    print ("FINISHED")
    cad.lcd.write("\nFINISHED")
    print_instructions()
    print_instructions_rasperry()  
    
def print_present():
    cad.lcd.clear()
    cad.lcd.set_cursor(0, 0)
    cad.lcd.write("3: PRESENTED")
    cad.lcd.write("\n4: NOT PRESENTED")
    print("Switch 3: Student presented")
    print ("Switch 4: Student didn´t present")
    

def print_sent_successfully():
    print("Sent Successfully")

def print_not_sent_successfully():
    print("Not sent successfully")

def save_offline(postString):
    global postStringArray
    postStringArray.append(postString)

def push_offline(self):
    global postStringArray
    for x in range (0, len(postStringArray)):
        try:
            p= requests.post(postStringArray[x])
            postStringArray.remove(postStringArray[x])
            print(p.text)
            cad.lcd.write(str(p.status_code))
        except requests.exceptions.RequestException as e:
            print ("A connection error occured")
            cad.lcd.clear()
            cad.lcd.set_cursor(0, 0)
            cad.lcd.write("\Conn.Err.")
            cad.lcd.write("\nTry again")
            print(postStringArray)
    print_instructions()
    print_instructions_rasperry() 

postStringArray = []
cad = pifacecad.PiFaceCAD() # display
cad.lcd.backlight_on() # Hintergrundbeleuchtung
cad.lcd.set_cursor(0, 0)  # set the cursor to the initial position
listener = pifacecad.SwitchEventListener(chip=cad)
listener.register(0, pifacecad.IODIR_FALLING_EDGE, qr_reader)
listener.register(2, pifacecad.IODIR_FALLING_EDGE, finish_aplication)
listener.register(3,pifacecad.IODIR_FALLING_EDGE, presented)
listener.register(4,pifacecad.IODIR_FALLING_EDGE, not_presented)
listener.register(1,pifacecad.IODIR_FALLING_EDGE, push_offline)
listener.activate()
print_instructions_rasperry()
print_instructions()    
