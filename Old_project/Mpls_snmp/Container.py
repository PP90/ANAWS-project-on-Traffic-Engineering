class Container(object):
	"""This class can represents both a single tunnel configuration or a LSP instance, with the relative informations"""
	def __init__(self, name):
		self._name = name
		self._info = {}
	
	
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
	
	def getName(self):
		return self._name
		
	"""This function returns the value of a given attribute passed as parameter <attrName>"""
	"""if there isn't a attribute named as <attrName>, it returns None"""
	def getAttribute(self, attrName):
		if attrName not in self._info.keys():
			return None
		return self._info[attrName]
		
	"""This function returns the entire dictionary of attribute"""
	"""The dictionary is structured as follow: {'Attr1' : val1, 'Attr2' : val2, ...}"""
	def getAttributeDict(self):
		return self._info
		
	
