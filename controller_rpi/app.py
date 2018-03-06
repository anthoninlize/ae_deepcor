import struct
import socket
import logging
from PIL import Image
import io
import subprocess as sp
import os
import signal
logging.basicConfig(level=logging.DEBUG)

class App:
    """
    Main App class to start on the controller Raspberry Pi. 
    """
    __remote_rpi_ip = "localhost"
    __remote_rpi_cmd_port = 1025
    __remote_rpi_video_port = 1024
    __connection = None
    __videostream_sp = None
    __pictures_folder = "./pictures/"

    def __init__(self):
        """
        Initializes an instance of this class.
        """
        pass
    
    def __recvall(self, sock, count):
        """
        Receives all bytes from a given buffer for a certain buffer size.
        """
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf
    
    def recv_message(self):
        """
        Receives data from the socket and interprete it as a message.
        """
        lengthbuf = self.__recvall(self.__connection, 4)
        length, = struct.unpack('!I', lengthbuf)
        data = self.__recvall(self.__connection, length)
        return data.decode("utf8")

    def send_message(self, message):
        """
        Sends a message preceding by its size.
        """
        l = len(message)
        self.__connection.sendall(struct.pack('!I', l))
        self.__connection.sendall(bytes(message, "utf8"))

    def startup(self):
        """
        Main function, starts the program on controller's side
        """
        ip = input("Remote RPI IP (enter to use localhost): ")
        if ip is not None and ip != "":
            self.__remote_rpi_ip = ip
        cmd_port = input("Remote RPI command port (enter to use 1025): ")
        if cmd_port is not None and cmd_port != "":
            self.__remote_rpi_cmd_port = int(cmd_port)
        video_port = input("Remote RPI video port (enter to use 1024): ")
        if video_port is not None and video_port != "":
            self.__remote_rpi_video_port = int(video_port)

        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection.connect((self.__remote_rpi_ip, self.__remote_rpi_cmd_port))
        logging.info("Connected to {}:{}, waiting for command inputs.".format(self.__remote_rpi_ip, self.__remote_rpi_cmd_port))
        cmd = input("")
        while cmd and cmd != "exit" and cmd != "shutdown":
            print("sending " + cmd)

            if cmd == "capture":
                # Need to stop livestream beforehand
                self.stop_livestream()
            # sending command
            self.send_message(cmd)
            # waiting for the response
            data = self.recv_message()
            logging.debug("received: " + data)
            result = self.process_response(data)
            if result is None:
                cmd = input("")
            else:
                cmd = result
        
        # sending shutdown command
        cmd = "shutdown"
        self.send_message(cmd)
        self.__connection.close()

    def process_response(self, message):
        """
        Process a response received from the server. 
        Based on the response, an action is returned to carry on through the main loop.
        """
        feedback = None
        if message == "videostarted":
            # Starts livestreaming the video
            self.start_livestream()
        elif message == "capturedone":
            file_name = self.recv_message()
            logging.debug("Receiving new image: " + file_name)
            self.recv_image(file_name)
            logging.debug("File saved!")
            feedback = "startvideo"
        return feedback
        
    def recv_image(self, file_name):
        """
        Receives bytes from the socket, interprets it as an image and stores it.
        """
        lengthbuf = self.__recvall(self.__connection, 4)
        length, = struct.unpack('!I', lengthbuf)
        data = self.__recvall(self.__connection, length)
        image = Image.open(io.BytesIO(data))
        image.save(self.__pictures_folder + file_name)

    def start_livestream(self):
        """
        Starts the video livestream and keeps a reference to the sub process created
        """
        cmd = "mplayer -fps 200 -demuxer h264es ffmpeg://tcp://{}:{}".format(self.__remote_rpi_ip, self.__remote_rpi_video_port)
        self.__videostream_sp = sp.Popen(cmd, stdout=sp.PIPE, shell=True, preexec_fn=os.setsid)
    
    def stop_livestream(self):
        """
        Ends the video livestream if currently operating
        """
        if self.__videostream_sp is not None:
            self.__videostream_sp.kill()
            os.killpg(os.getpgid(self.__videostream_sp.pid), signal.SIGTERM) 
            self.__videostream_sp = None


