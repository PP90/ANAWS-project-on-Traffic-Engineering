class Container(object):
	"""This class can represents both a single tunnel configuration or a LSP instance, with the relative informations"""
	def __init__(self, name):
		self._name = name
		self._info = {}
	
	def getName(self):
		return self._name
	
	"""It adds a new entry in the dictionary '_info' and it returns the inserted value, if it is empty, 
	otherwise it returns the current value"""
	def addInfo(self, info, value):
		if(info in self._info.keys()):
			return self._info[info]
		else:
			self._info[info] = value
			return self._info[info]
	
	def __str__(self):
		returnString = "Name: " + self._name + '\n'
		for elem in sorted(self._info.keys()):
			returnString += '\t' + elem + ": " + str(self._info[elem]) + '\n'
		return returnString
	
