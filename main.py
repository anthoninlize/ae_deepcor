#/usr/bin/python3.5
import sys
from datetime import datetime
import time
import paramiko


import liveview
import capture
import img_transfer
import insert_info_to_image
import ipdb

from input import *

sys.path.insert(0, './sensors/lux_sensor')
sys.path.insert(0, './sensors/pressure_sensor')
sys.path.insert(0, './sensors/temp_sali_sensors')

#import lux
import pressure
import temp_sali

# Date and Time acquisition and format
timestamp = datetime.now()
timestamp_2 = '{}-{}-{} {}:{}:{}'.format(timestamp.day, timestamp.month,timestamp.year, timestamp.hour, timestamp.minute, timestamp.second)


# SSH remote connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    ip_remote,
    username=username_remote,
    password=password_remote
)

# SCP 
scp = SCPClient(ssh.get_transport())

# Live view
liveview.liveview_on(lv_fps,ssh,ip_local)
while True :
    #time.sleep(5)
    key = input("\nLoading liveview... \nPress 'q' to quit Liveview, press 'c' for capture:")
    if key == 'q':
        print('\nLiveview ended...')
        exit()
    elif key == 'c':
        liveview.liveview_off(ssh)
        print('\nLiveview ended...')
        break
    
# Capture picture   
print('\nCapture...')

raw_file = '{}{}{}_{}h{}m{}s.jpeg'.format(
    timestamp.year,
    timestamp.month,
    timestamp.day,
    timestamp.hour,
    timestamp.minute,
    timestamp.second
)

capture.capture(ssh,raw_file)

# Data transfer from remote to local
