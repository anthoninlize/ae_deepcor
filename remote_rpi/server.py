import logging
logging.basicConfig(level=logging.DEBUG)
import socket
from camera_interface import Liveview

class Server:
	"""
	Defines all the behavior of the socket server running on the remote Raspberry Pi.
	"""
	__ip = "169.254.111.142"
	__port = 1025
	__bufferSize = 16
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
			while not(shouldShutdownServer):
				bufferedData = ""

				# Receive the data in small chunks and retransmit it
				remainingData = True
				data = ""
				while remainingData:
					bufferedData = self.__connection.recv(self.__bufferSize)
					
					if bufferedData and not(bufferedData.endswith("\n")):
						data += bufferedData
					else:
						data += bufferedData
						remainingData = False

						if data.startswith("shutdown"):
							shouldShutdownServer = True
						else:
							self.processCommand(data.replace('\n', ''))
		except Exception as e:
			logging.error("Error: ")
			logging.error(e)

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
			commandParameters = {"width": None, "height": None, "fps": None}
			parts = command.split(" ")
			for part in parts:
				param = part.split("=")
				if param[0] in commandParameters.keys():
					commandParameters[param[0]] = param[1]
			self.__liveview.startVideo(**commandParameters)

		elif command.startswith("capture"):
			commandParameters = {"width": None, "height": None}
			parts = command.split(" ")
			for part in parts:
				param = part.split("=")
				if param[0] in commandParameters.keys():
					commandParameters[param[0]] = param[1]
			self.__liveview.capture(**commandParameters)
