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
from scp import SCPClient

from input import *

sys.path.insert(0, './sensors/lux_sensor')
sys.path.insert(0, './sensors/pressure_sensor')
sys.path.insert(0, './sensors/temp_sali_sensors')

#import lux
import pressure
import temp_sali

#-------------------- Date and Time acquisition and format----------------------
timestamp = datetime.now()
timestamp_2 = '{}-{}-{} {}:{}:{}'.format(timestamp.day, timestamp.month,timestamp.year, timestamp.hour, timestamp.minute, timestamp.second)


#------------------------- SSH remote connection--------------------------------
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    ip_remote,
    username=username_remote,
    password=password_remote
)


#-------------------------------- Open SCP -------------------------------------
scp = SCPClient(ssh.get_transport())


# ------------------------------- Live view-------------------------------------
# liveview.liveview_on(lv_fps,ssh,ip_local)
# while True :
#     key = input("\nLoading liveview... \nPress 'q' to quit Liveview, press 'c' for capture:")
#     if key == 'q':
#         print('\nLiveview ended...')
#         exit()
#     elif key == 'c':
#         liveview.liveview_off(ssh)
#         print('\nLiveview ended...')
#         break

# -------------------------------Image capture----------------------------------
# print('\nCapture...')
# 
# raw_file = '{}{}{}_{}h{}m{}s.jpeg'.format(
#     timestamp.year,
#     timestamp.month,
#     timestamp.day,
#     timestamp.hour,
#     timestamp.minute,
#     timestamp.second
# )
# 
# capture.capture(ssh,raw_file,remote_img_path)

# -----------------------  Remote measurements -----------------------
# add  __init__.py in sensor folders
# le code ci-dessous est degueu... mais il marche :p

# Get salinity
cmd_s="cd CodeDeepcor; python -c  'from temp_sali_sensors import temp_sali; print temp_sali.get_sali()'"
ssh_stdin,ssh_stdout,ssh_stderr = ssh.exec_command(cmd_s)
salinity = float(ssh_stdout.readlines()[0][0:-1])

# Get salinity
cmd_t="cd CodeDeepcor; python -c  'from temp_sali_sensors import temp_sali; print temp_sali.get_temp()'"
ssh_stdin,ssh_stdout,ssh_stderr = ssh.exec_command(cmd_t)
temperature = float(ssh_stdout.readlines()[0][0:-1])

# Get pressure
cmd_p = "cd CodeDeepcor; python -c 'from pressure_sensor import pressure; print pressure.get_pressure()'"
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_p)
pressure = float(ssh_stdout.readlines()[0][0:-1])

# Get luminosity
cmd_l = "cd CodeDeepcor; python -c 'from lux_sensor import lux; print lux.get_lux()'"
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_l)
lux = float(ssh_stdout.readlines()[0][0:-1])

print("Luminosity: %0.2f" %lux)
print("Pressure: %0.2f" %pressure)
print("Temperature: %0.2f" %temperature)
print("Salinity: %0.2f" %salinity)
ipdb.set_trace()

# ---------------------------  GPS measurements -------------------------------

# Data transfer from remote to local
