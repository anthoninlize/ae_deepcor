#For help, consult https://circuitdigest.com/microcontroller-projects/raspberry-pi-3-gps-module-interfacing

#!/usr/bin/env python

import sys
import serial
import time

def get_gps():
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = '/dev/ttyAMA0'
    ser.timeout = 1

    ser.open()

    if not ser.isOpen():
        print("Unable to open serial port!")
        raise SystemExit
    
    while True:
        gps = ser.readline()
        if gps[:6] == '$GPRMC':
            result = gps
            break
           
    gps_coord = result.split(",")
    latitude_angle  = float(gps_coord[3]) / 100
    latitude_ns     = gps_coord[4]
    longitude_angle = float(gps_coord[5]) / 100
    longitude_we    = gps_coord[6]
    
    ser.close()
    
    return [latitude_angle, latitude_ns, longitude_angle, longitude_we]