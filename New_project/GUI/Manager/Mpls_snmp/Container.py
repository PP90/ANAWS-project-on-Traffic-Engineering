"""
Copyright (c) 2016, Pietro Piscione, Luigi De Bianchi, Giulio Micheloni
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * The names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL P. PISCIONE, L. DE BIANCHI, G. MICHELONI BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
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
		
	def setAttribute(self, attrName, value):
		if attrName not in self._info.keys():
			return None
		self._info[attrName] = value
		return self._info[attrName]
		
	"""This function returns the entire dictionary of attribute"""
	"""The dictionary is structured as follow: {'Attr1' : val1, 'Attr2' : val2, ...}"""
	def getAttributeDict(self):
		return self._info
		
	
