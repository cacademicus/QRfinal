# inspired by instructions of https://blog.milsystems.de/2013/08/wie-benutze-ich-die-raspberry-pi-als-qr-code-lesegeraet/
#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
Reads QR-Codes
'''
import os, signal, subprocess

strfile1 = ("qrcode")

def read():
    zbarcam=subprocess.Popen("zbarcam --raw --nodisplay /dev/video0", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    print ("zbarcam started successfully...")
    
    while True:
        qrcodetext=zbarcam.stdout.readline()
        if qrcodetext!="":
            print ("success")
            break

    os.killpg(zbarcam.pid, signal.SIGTERM)  # Prozess stoppen
    print ("zbarcam stopped successfully")
    return qrcodetext