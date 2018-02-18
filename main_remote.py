"""
Main process of the remote Raspberry Pi. Starts a video broadcasting and listen to user's command on a local socket server.
"""
from remote_rpi.app import App

#sp.Popen(
#    raspividCmd,
#    shell=True,
#    stdout=sp.PIPE,
#    stderr= sp.PIPE
#)


if __name__ == "__main__":
    app = App()
    app.startup()