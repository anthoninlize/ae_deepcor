"""
Main process of the controller Raspberry Pi. 
Listens to user's commands and livestreams the video from the other Raspberry Pi.
"""
from controller_rpi.app import App

#sp.Popen(
#    raspividCmd,
#    shell=True,
#    stdout=sp.PIPE,
#    stderr= sp.PIPE
#)


if __name__ == "__main__":
    app = App()
    app.startup()