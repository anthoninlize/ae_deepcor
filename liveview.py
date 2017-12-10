import subprocess as sp
import time

def liveview_on(fps,ssh,ip_local):
    
    # local
    cmd1 = "nc -l -p 5001 | /usr/bin/mplayer -fps {0} -cache 1024 -".format(fps)
    p = sp.Popen(
        cmd1,
        shell=True,
        stdout=sp.PIPE,
        stderr= sp.PIPE
    )
    
    # remote
    cmd2 = "raspivid -t 0 -w 1280 -h 720 -fps {0} -o - | nc {1} 5001".format(fps,ip_local)
    ssh.exec_command(cmd2)

def liveview_off(ssh):
    
    cmd = "kill $(ps -e | grep raspi | awk '{print $1}')"
    ssh.exec_command(cmd)
    
    #for line in p.stdout:
      #  print(">> "+ str(line.rstrip()))
        #p.stdout.flush()
    

    
# if __name__ == '__main__':
#     liveview(5, '169.254.111.142','169.254.39.64')
#     try:
#         while True :
#             time.sleep(5)
#     except KeyboardInterrupt:
#         pass

        
        