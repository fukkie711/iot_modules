# -*- coding: utf-8 -*-
import os
import sys
import glob
import time
import datetime
import re
import subprocess
import spidev
import RPi.GPIO as GPIO
spi = spidev.SpiDev()
spi.open(0, 0) #port 0, cs0
Vref = 3.29476

def get_soil_moisture():
    #get data from a dtermined channel
    adc = spi.xfer2([0x68,0x00])
    #data = ((adc[0] & 3) << 8) | adc[1]
    data = (adc[0] * 256 + adc[1]) & 0x3ff
    #data = (adc[0] * 256 + adc[1])
    return adc
'''if __name__ == '__main__':
    print("soil moisture: ", get_soil_moisture())
'''
try:
    while True:
        print("soil moisture: ", get_soil_moisture())
        time.sleep(1)
except KeyboardInterrupt:
    pass
spi.close()
