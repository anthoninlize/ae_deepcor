import os
import signal
import subprocess as sp
from datetime import datetime
#from image_editor import ImageEditor
import logging
logging.basicConfig(level=logging.DEBUG)

class Liveview:
	"""
	Defines the different commands to control the liveview
	"""
	__broadcastingPort = 1024
	__videoFps = 20
	__videoImageWidth = 640
	__videoImageHeight = 360
	__videoSh = 0
	__videoCo = 0
	__videoBr = 50
	__videoSa = 0
	__videoISO = 100
	__videoEV = 0

	__pictureCo = 0
	__pictureBr = 50
	__pictureSa = 20
	__pictureISO = 400
	__pictureEV = -2
	__pictureImageWidth = 640
	__pictureImageHeight = 360
	__pictureFilePath = "/home/pi/workspace/pictures/"
	__pictureFileNamePattern = "{datetime}_raw.jpg"
	__currentFileName = None

	__videoSubprocess = None


	def __init__(self):
		"""
		Constructor of the class
		"""
		# Testing if picture folder exists, creating it otherwise
		if not os.path.isdir(self.__pictureFilePath):
			os.makedirs(self.__pictureFilePath)
		#subdirIteration = 1
		#if os.path.isdir(self.__pictureFilePath + str(subdirIteration) + "/"):
		#	subdirIteration += 1
		#self.__pictureFilePath += str(subdirIteration) + "/"
		#os.makedirs(self.__pictureFilePath)


	def __getRaspividCommand(self, broadcastingPort, width, height, fps):
		"""
		Builds a shell command based in input paramaters
		"""
		return ("raspivid -n -t 0 -w " + str(width) + " -h " + str(height) + 
			" -fps " + str(fps) + " -l -o tcp://0.0.0.0:" + str(broadcastingPort) + 
			" -sh 0 -co " + str(self.__videoCo) + " -br " + str(self.__videoBr) +
			" -sa " + str(self.__videoSa) + " -ISO " + str(self.__videoISO) +
			" -ev " + str(self.__videoEV))

	def __getRaspistillCommand(self, width, height):
		"""
		Builds a shell command based in input paramaters
		"""
		now = datetime.utcnow()
		self.__currentFileName = self.__pictureFileNamePattern.format(datetime=now.strftime("%Y%m%d-%H%M%S"))
		return ("raspistill -n -t 1 -w " + str(width) + " -h " + str(height)
			+ " -o " + self.__pictureFilePath 
			+ self.__currentFileName + " -sh 0 -co " + str(self.__pictureCo) + " -br " + str(self.__pictureBr) +
			" -sa " + str(self.__pictureSa) + " -ISO " + str(self.__pictureISO) +
			" -ev " + str(self.__pictureEV))
			
	def getPicturePath(self):
		return self.__pictureFilePath

	def startVideo(self, **kwargs):
		"""
		Starts a video broadcasting, kills the existing one if any.
		"""
		# Killing existing process
		self.endVideo()

		if "width" in kwargs.keys():
			if kwargs["width"] is not None:
				self.__videoImageWidth = kwargs["width"]
		if "height" in kwargs.keys():
			if kwargs["height"] is not None:
				self.__videoImageHeight = kwargs["height"]
		if "fps" in kwargs.keys():
			if kwargs["fps"] is not None:
				self.__videoFps = kwargs["fps"]
		if "co" in kwargs.keys():
			if kwargs["co"] is not None:
				self.__videoCo = kwargs["co"]
		if "br" in kwargs.keys():
			if kwargs["br"] is not None:
				self.__videoBr = kwargs["br"]
		if "sa" in kwargs.keys():
			if kwargs["sa"] is not None:
				self.__videoSa = kwargs["sa"]
		if "iso" in kwargs.keys():
			if kwargs["iso"] is not None:
				self.__videoISO = kwargs["iso"]
		if "ev" in kwargs.keys():
			if kwargs["ev"] is not None:
				self.__videoEV = kwargs["ev"]

		# Starting video broadcasting
		cmd = self.__getRaspividCommand(self.__broadcastingPort, 
			self.__videoImageWidth, self.__videoImageHeight, self.__videoFps)

		logging.debug("Starting video broadcasting with the following cmd: " + cmd)

		self.__videoSubprocess = sp.Popen(cmd, stdout=sp.PIPE, shell=True, preexec_fn=os.setsid)

	def endVideo(self):
		"""
		Closes the video broadcasting if existing
		"""
		if self.__videoSubprocess is not None:
			self.__videoSubprocess.kill()
			os.killpg(os.getpgid(self.__videoSubprocess.pid), signal.SIGTERM) 
			self.__videoSubprocess = None

	def capture(self, **kwargs):
		"""
		Captures an image after killing the video broadcasting,then restarts it.
		"""
		# Killing existing process
		self.endVideo()

		if "width" in kwargs.keys():
			if kwargs["width"] is not None:
				self.__pictureImageWidth = kwargs["width"]
		if "height" in kwargs.keys():
			if kwargs["width"] is not None:
				self.__pictureImageHeight = kwargs["height"]
		if "co" in kwargs.keys():
			if kwargs["co"] is not None:
				self.__pictureCo = kwargs["co"]
		if "br" in kwargs.keys():
			if kwargs["br"] is not None:
				self.__pictureBr = kwargs["br"]
		if "sa" in kwargs.keys():
			if kwargs["sa"] is not None:
				self.__pictureSa = kwargs["sa"]
		if "iso" in kwargs.keys():
			if kwargs["iso"] is not None:
				self.__pictureISO = kwargs["iso"]
		if "ev" in kwargs.keys():
			if kwargs["ev"] is not None:
				self.__pictureEV = kwargs["ev"]

		# Capturing image
		cmd = self.__getRaspistillCommand(self.__pictureImageWidth, self.__pictureImageHeight)
		logging.debug("Capturing image with the following command: " + cmd)
		sp.Popen(cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL, shell=True)
		
		return self.__currentFileName

		#imageEditor = ImageEditor()
		#imageEditor.getMeasurements()
