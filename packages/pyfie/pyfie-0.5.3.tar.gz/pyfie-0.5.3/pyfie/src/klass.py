import pyfie.src.vars as vars

class locker:
	def __init__(self, path, value):
		self.__valueOfFile = value
		self.pathToFile = path
		vars.curr = self.__dict__
		self.__dict__ = {}

	def fetch(self, password):
		self.__dict__ = vars.curr
		if self.pathToFile in vars.keys and vars.keys[self.pathToFile] == password:
			return self.__valueOfFile
			self.__dict__ = {}