import paramiko
from scp import SCPClient

import time

def img_transfer(scp,filename):
 
    # remote
    scp.get(
        '/home/pi/deepcor_images/{0}'.format(filename), 'pictures/raw/'
    )
    print("Image transfer done!")


if __name__ == '__main__':
    img_transfer('169.254.111.142','169.254.39.64','test.jpg')


        
        