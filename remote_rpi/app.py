from .server import Server

class App:
	"""
	Main App class to start on the remote Raspberry Pi. Will handle server
	startup, shutdown, command relaying to server.
	"""
	__server = None

	def __init__(self):
		"""
		Initializes an instance of this class
		"""
		self.__server = Server()

	def startup(self):
		self.__server.startServer()