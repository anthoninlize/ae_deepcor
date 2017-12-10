import os

def capture(ssh,filename,remote_img_path):
 
    # remote

    cmd2 = "raspistill -o {0}/{1}".format(remote_img_path,filename)
    print("in {0}/{1}".format(remote_img_path,filename))
    ssh.exec_command(cmd2)
    
    # list = scp.get()
    # 
    # if filename in os.chdir(remote_img_path):
    #     print('\nPhoto saved as {0}!'.format(filename))
    # else
    #     print('ERROR:photo not saved!')
    # 

    
