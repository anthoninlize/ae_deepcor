import logging
logging.basicConfig(level=logging.DEBUG)
import socket
import struct
import os
import time
from .camera_interface import Liveview

class Server:
	"""
	Defines all the behavior of the socket server running on the remote Raspberry Pi.
	"""
	__ip = ""
	__port = 1025
	__bufferSize = 1024
	__socket = None
	__connection = None

	__liveview = None

	def __init__(self, **kwargs):
		"""
		Contructor of the class
		"""
		if "port" in kwargs.keys():
			self.__port = kwargs['port']

		# Initializing liveview instance
		self.__liveview = Liveview()

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
		if lengthbuf is None:
			return "connectionbroken"
		else:
			length, = struct.unpack('!I', lengthbuf)
			data = self.__recvall(self.__connection, length)
			return data.decode("utf8")

	def send_message(self, message):
		l = len(message)
		self.__connection.sendall(struct.pack('!I', l))
		self.__connection.sendall(bytes(message, "utf8"))

	def startServer(self):
		"""
		Starts the server and handles incoming commands.
		"""
		# Create a TCP/IP socket
		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Bind the socket to the port
		serverAddress = (self.__ip, self.__port)
		logging.debug("Sarting server on port {}".format(self.__port))
		self.__socket.bind(serverAddress)

		# Starting socket server
		self.__socket.listen(1)
		shouldShutdownServer = False

		logging.debug("Waiting for client connection...")
		self.__connection, clientAddress = self.__socket.accept()
		logging.debug("Connected client: ")
		logging.debug(clientAddress)
		try:
			client_connected = True
			while not(shouldShutdownServer):
				if not client_connected:
					logging.debug("Waiting for client connection...")
					self.__connection, clientAddress = self.__socket.accept()
					logging.debug("Connected client: ")
					logging.debug(clientAddress)
					client_connected = True
				data = self.recv_message()
				logging.debug("received: " + data)

				if data == "shutdown":
					shouldShutdownServer = True
				elif data == "connectionbroken":
					client_connected = False
				else:
					self.processCommand(data.replace('\n', ''))
					
		except Exception as e:
			logging.error("Error: ")
			logging.error(e)
			raise
		finally:
			self.closeServer()


	def closeServer(self):
		"""
		Closes the socket
		"""
		self.__liveview.endVideo()
		# Closing the connection
		logging.debug("Closing connection...")
		self.__connection.shutdown(socket.SHUT_RDWR)
		self.__connection.close()
		logging.debug("Connection closed...")
		# Closign the socket
		logging.debug("Closing socket...")
		# Telling the system that no more buffered data is expected
		self.__socket.shutdown(socket.SHUT_RDWR)
		# Actually closing the socket
		self.__socket.close()
		logging.debug("Socket closed.")

	def processCommand(self, command):
		"""
		Parses the command and relay instruction to relevant parties.
		"""
		logging.debug(command)

		if command.startswith("startvideo"):
			commandParameters = {"width": None, "height": None, "fps": None, "co": None, "br": None, "sa": None, "iso": None, "ev": None}
			parts = command.split(" ")
			for part in parts:
				param = part.split("=")
				if param[0] in commandParameters.keys():
					commandParameters[param[0]] = param[1]
			self.__liveview.startVideo(**commandParameters)

			self.send_message("videostarted")

		elif command.startswith("capture"):
			commandParameters = {"width": None, "height": None, "co": None, "br": None, "sa": None, "iso": None, "ev": None}
			parts = command.split(" ")
			for part in parts:
				param = part.split("=")
				if param[0] in commandParameters.keys():
					commandParameters[param[0]] = param[1]
			file_name = self.__liveview.capture(**commandParameters)
			# TODO : get the pictures path from the camera_interface, or store it there and access it from the camera_interface
			filepath = self.__liveview.getPicturePath() + file_name
			self.send_message("capturedone")
			logging.debug("sending filename...")
			time.sleep(1)
			self.send_message("controller_" + file_name)
			logging.debug("sending file...")
			self.send_image(filepath)

		elif command.startswith("endvideo"):
			self.__liveview.endVideo()
			self.send_message("videoended")
		else:
			self.send_message("unknown command received")
	
	def send_image(self, file_name):
		"""
		Sends the given image through the socket, preceding by its size.
		"""
		with open(file_name, "rb") as image_file:
			f = image_file.read()
			b = bytearray(f)
			l = len(b)
			self.__connection.sendall(struct.pack('!I', l))
			self.__connection.sendall(b)
