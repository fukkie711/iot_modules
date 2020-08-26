# -*- coding: utf-8 -*-
import sys
import serial # 'pip3 install pyserial' before use it
import time
import subprocess
import getrpimodel
import datetime
from time import sleep
import RPi.GPIO as GPIO

if getrpimodel.model() == "3 Model B":
    serial_dev = '/dev/ttyS0'
    stop_getty = 'sudo systemctl stop serial-getty@ttyS0.service'
    start_getty = 'sudo systemctl start serial-getty@ttyS0.service'
else:
    serial_dev = '/dev/ttyAMA0'
    stop_getty= 'sudo systemctl stop serial-getty@ttyAMA0.service'
    start_getty = 'sudo systemctl start serial-getty@ttyAMA0.service'

def mh_z19():
    ser = serial.Serial(serial_dev,
                         baudrate = 9600,
                         bytesize = serial.EIGHTBITS,
                         parity = serial.PARITY_NONE,
                         stopbits = serial.STOPBITS_ONE,
                         timeout=1.0)
    
    while 1:
        result=ser.write(b'\xff\x01\x86\x00\x00\x00\x00\x00\x79')
        s = ser.read(9)
        print('Raw data check:', s)
        if len(s)!=0 and s[0] == "\xff" and s[1] == "\x86":
            return {'co2': (s[2])*256 + (s[3])}
            break
        else:
            return {'co2': (s[2])*256 + 1000}
        break
    
def main():
    subprocess.call(stop_getty,stdout=subprocess.PIPE, shell=True)
    subprocess.call(start_getty,stdout=subprocess.PIPE, shell=True)
    while(1):
        
        now = datetime.datetime.now()
        now_ymdhms = "{0:%Y/%m/%d %H:%M:%S}".format(now)
        
        #Get Date
        value = mh_z19()
        co2 = value['co2']
        print('CO2:', co2)
                
        sleep(1)
if __name__ == '__main__':
    main()
