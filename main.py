#/usr/bin/python3.5
"""
Script principal appelant les méthodes de :
- connexion en SSH au 2eme raspberryPI (en profondeur)
- streaming de la video
- capture d'image et copie de la photo
- mesures des 4 capteurs en profondeur
- copie des données en surface et enregistrement en CSV
- ecriture des données sur la photo
Reste à implémenter :
- import des données GPS en surface
"""
import sys
from datetime import datetime
import time
import paramiko


import liveview
import capture
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

timestamp = datetime.now()


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
liveview.liveview_on(lv_fps,ssh,ip_local)
while True :
    key = input("\nLoading liveview... \nPress 'q' to quit Liveview, press 'c' for capture:")
    if key == 'q':
        print('\nLiveview ended...')
        exit()
    elif key == 'c':
        liveview.liveview_off(ssh)
        print('\nLiveview ended...')
        break

# -------------------------------Image capture----------------------------------

print('\nCapture...')

raw_file = '{}{}{}_{}h{}m{}s.jpeg'.format(
    timestamp.year,
    timestamp.month,
    timestamp.day,
    timestamp.hour,
    timestamp.minute,
    timestamp.second
)

capture.capture(ssh,raw_file,remote_img_path)
time.sleep(5)


# -----------------------  Remote measurements -----------------------
# add  __init__.py in sensor folders
# le code ci-dessous est degueu... mais il marche :p

print('\nMeasurements...')

# Get salinity
cmd_s="cd CodeDeepcor; python -c  'from temp_sali_sensors import temp_sali; print temp_sali.get_sali()'"
ssh_stdin,ssh_stdout,ssh_stderr = ssh.exec_command(cmd_s)
salinity = float(ssh_stdout.readlines()[0][0:-1])

# Get temperature
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

print("\nLuminosity: %0.2f" %lux)
print("Pressure: %0.2f" %pressure)
print("Temperature: %0.2f" %temperature)
print("Salinity: %0.2f" %salinity)

# ---------------------------  GPS measurements -------------------------------

print('\nGPS measurements...')
gps_coord = 'to be measured'

# ---------------------Data transfer from remote to local----------------------
print('{0}/{1}'.format(remote_img_path,raw_file))
scp.get('{0}/{1}'.format(remote_img_path,raw_file),local_rawimg_path)
print("\nImage transfer done!")

# -------------------------- Save data in csv ---------------------------

# Date and Time acquisition and format
timestamp = '{}-{}-{} {}:{}:{}'.format(
    timestamp.day, 
    timestamp.month,
    timestamp.year, 
    timestamp.hour, 
    timestamp.minute, 
    timestamp.second
)

# Saving data in files

print("\nSaving data in csv...")
fcsv = open('csv/data_all.csv', 'a')
fcsv.write('{};{};{};{};{};{}\n'.format(timestamp, lux, pressure, temperature, salinity, raw_file))
fcsv.close()

fcsv = open('csv/data_one.csv', 'w')
fcsv.write('{};{};{};{};{};{}\n'.format(timestamp, lux, pressure, temperature, salinity, raw_file))
fcsv.close()

# ------------------------ Write data on image ---------------------------
print("\nWritting data on image...")
insert_info_to_image.add_banner(local_rawimg_path, local_modimg_path, timestamp, gps_coord, str(lux), str(pressure), str(temperature), str(salinity), raw_file)

print("\nEnd of program !")

scp.close()
ssh.close()
