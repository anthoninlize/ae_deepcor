import struct
import socket

class App:
    """
    Main App class to start on the controller Raspberry Pi. 
    """
    __remote_rpi_ip = None
    __remote_rpi_cmd_port = None
    __remote_rpi_video_port = None
    __connection = None

    def __init__(self):
        """
        Initializes an instance of this class
        """
        pass
    
    def __recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf
    
    def recv_message(self):
		lengthbuf = self.__recvall(self.__connection, 4)
		length, = struct.unpack('!I', lengthbuf)
		data = self.__recvall(self.__connection, length)
		return data.decode("utf8")

	def send_message(self, message):
		l = len(message)
		self.__connection.sendall(struct.pack('!I', l)
		self.__connection.sendall(bytes(message, "utf8"))

    def startup(self):
        self.__remote_rpi_ip = input("Remote RPI IP: ")
        self.__remote_rpi_cmd_port = int(input("Remote RPI command port: "))
        self.__remote_rpi_video_port = int(input("Remote RPI video port: "))

        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection.connect((self.__remote_rpi_ip, self.__remote_rpi_cmd_port))
        print("Connected to {}:{}, waiting for command inputs.".format(self.__remote_rpi_ip, self.__remote_rpi_cmd_port))
        cmd = input("")
        while cmd and cmd != "exit":
            print("sending " + cmd)

            # sending command
            self.send_message(cmd)
            # waiting for the response
            data = self.recv_message()
            self.process_response(data)

            cmd = input("")
        
        # sending shutdown command
        cmd = "shutdown"
        self.send_message(cmd)
        self.__connection.close()

    def process_response(self, message):
        if message == "videostarted":
            # Starts livestreaming the video
            pass
        elif message = "capturedone":
            #
            pass
        

