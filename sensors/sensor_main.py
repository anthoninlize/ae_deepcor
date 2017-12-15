"""
Script de test d'importation des données des 4 capteurs.
Non utilisé car le code a été copié dans le 'main' 
"""

import sys
from datetime import datetime

sys.path.insert(0, './lux_sensor')
sys.path.insert(0, './pressure_sensor')
sys.path.insert(0, './temp_sali_sensors')
sys.path.insert(0, './insert_info_to_image')
import lux
import pressure
import temp_sali
import insert_info_to_image
    
lux         = lux.get_lux()
pressure    = pressure.get_pressure()
temperature = temp_sali.get_temp()
salinity    = temp_sali.get_sali()

picture_name = 'raw_picture.jpeg' #in waiting for the true picture

# Date and Time acquisition and format
timestamp = datetime.now()
timestamp = '{}-{}-{} {}:{}:{}'.format(timestamp.day, timestamp.month,timestamp.year, timestamp.hour, timestamp.minute, timestamp.second)
                
# Saving data in files
#fcsv = open('/home/public/data_all.csv', 'a')
fcsv = open('csv/data_all.csv', 'a')
fcsv.write('{};{};{};{};{};{}\n'.format(timestamp, lux, pressure, temperature, salinity, picture_name))
fcsv.close()
#fcsv = open('/home/public/data_one.csv', 'w')
fcsv = open('csv/data_one.csv', 'w')
fcsv.write('{};{};{};{};{};{}\n'.format(timestamp, lux, pressure, temperature, salinity, picture_name))
fcsv.close()

print("Luminosity: %0.2f" %lux)
print("Pressure: %0.2f" %pressure)
print("Temperature: %0.2f" %temperature)
print("Salinity: %0.2f" %salinity)

insert_info_to_image.add_banner(timestamp, str(lux), str(pressure), str(temperature), str(salinity), picture_name)
