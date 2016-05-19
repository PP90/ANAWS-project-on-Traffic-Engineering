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
from Container import *
from snmpWrapper import *
from Oid import *
from ipaddress import *

class TeTunnels(object):
	"""This class implements the algorithm for getting the configured tunnels and LSP in the network"""
	
	def __init__(self, routerAddress, communityString):
		self._rAddress = routerAddress
		self._cString = communityString
		self._ConfiguredTunnels = {}
		self._LspTable = {}
		self._NameIdMap = {}
		self._LspIdMap = {}
	
	def getConfTunnels(self):
		return self._ConfiguredTunnels
	
	def getLspTable(self):
		return self._LspTable
	
	def start(self):
		"""This function executes the algorithm and it populates the two tables"""
		#First of all, clear the data structure
		self._ConfiguredTunnels = {}
		self._LspTable = {}
		self._NameIdMap = {}
		self._LspIdMap = {}
		
		"""First phase: get the configured tunnel names"""
		self._getTunnelName()
		"""2nd phase: get the LSP descriptive name"""
		self._getLspDescr()
		"""3rd phase: get the path for each configured tunnel"""
		self._getTunnelPaths()
		"""4th phase: populate the LSP table with every needed information"""
		self._populateLspTable()
		
		
	def _parse_oid(self, response_oid):
		"""The OID for mpls-te is composed as follows: 'resource_oid.tunnel_id.tunnel_instance.source_ip_address.destination_ip_address'"""
		resource = response_oid[:-4]
		#the ip addresses are in decimal format, so they need convertion
		dest_ip = str(ip_address(response_oid[-1]))
		source_ip = str(ip_address(response_oid[-2]))
		tun_instance = response_oid[-3]
		tun_id = response_oid[-4]
		return resource, tun_id, tun_instance, source_ip, dest_ip
		
	def _getTunnelName(self):
		oid = string_to_OID("mplsTunnelName")
		walk = snmpwalk(oid, self._rAddress, self._cString)
		row = next_record(walk)
		while row != None:
			#the row is actually a matrix with a single row: [[name],[val]]
			name = row[0][0]
			val = row[0][1]
			#Stop condition
			if val.prettyPrint() == 'No more variables left in this MIB View':
				break
			#Parse the responsed oid
			res, tun_id,tun_instance, source_ip, dest_ip = self._parse_oid(name)
			#Analyze only the rows regarding to tunnel head configurations
			if tun_instance == 0:
				index = str(tun_id) + '.' + str(tun_instance)
				tunnelName = val.prettyPrint()
				#add the mapping between "tunID.tunInst" <--> "TunnelName"
				self._NameIdMap[index] = tunnelName
				#add an object to the dictionary "_ConfiguredTunnels"
				confTun = Container(tunnelName)
				confTun.addInfo("Source Addr", source_ip)
				confTun.addInfo("Dest Addr", dest_ip)
				self._ConfiguredTunnels[tunnelName] = confTun
				
			row = next_record(walk)
		
	def _getLspDescr(self):
		oid = string_to_OID("mplsTunnelDescr")
		walk = snmpwalk(oid, self._rAddress, self._cString)
		row = next_record(walk)
		while row != None:
			#the row is actually a matrix with a single row: [[name],[val]]
			name = row[0][0]
			val = row[0][1]
			#Stop condition
			if val.prettyPrint() == 'No more variables left in this MIB View':
				break
			#Parse the responsed oid
			res, tun_id,tun_instance, source_ip, dest_ip = self._parse_oid(name)
			#Analyze the rows regarding to tunnel head configurations
			if tun_instance == 0:
				#using the index "TunID.TunInst" find the tunnelName and use it 
				#in order to add the descriptive name to the right entry in the dictionary
				index = str(tun_id) + '.' + str(tun_instance)
				tunnelDescr = val.prettyPrint()
				tunnelName = self._NameIdMap[index]
				self._ConfiguredTunnels[tunnelName].addInfo("Descriptive Name", tunnelDescr)
			#Analyze the rows regarding to LSP instance
			else:
				index = str(tun_id) + '.' + str(tun_instance)
				tunnelDescr = val.prettyPrint()
				#add the mapping between "tunID.tunInst" <--> "Tunnel Descriptive Name"
				self._LspIdMap[index] = tunnelDescr
				#add an object to the dictionary "_LspTable"
				LspInstance = Container(tunnelDescr)
				LspInstance.addInfo("Source", source_ip)
				LspInstance.addInfo("Dest", dest_ip)
				self._LspTable[tunnelDescr] = LspInstance
			row = next_record(walk)
	
	def _getValueFromResponse(self, response):
		record = next_record(response)
		if record == -1:
			return
		result = record[0][1].prettyPrint()
		if result == 'No more variables left in this MIB View':
			return None
		else:
			return result
	
	def _getConfiguredPath(self, prim_index, second_index, table):
		"""Get the path from the specified table: mplsTunnelHopTable (configured path) or mplsTunnelCHopTable (computed path)"""
		if table ==  "mplsTunnelHopTable":
			oidList = ['mplsTunnelHopAddrType','mplsTunnelHopIpv4Addr','mplsTunnelHopIpv6Addr', 'mplsTunnelHopIpv4PrefixLen', 'mplsTunnelHopIpv6PrefixLen']
		elif table == "mplsTunnelCHopTable":
			oidList = ['mplsTunnelCHopAddrType','mplsTunnelCHopIpv4Addr','mplsTunnelCHopIpv6Addr', 'mplsTunnelCHopIpv4PrefixLen', 'mplsTunnelCHopIpv6PrefixLen']
		hops = []
		singleHop = ''
		addrPrefix = 0
		oid = string_to_OID(oidList[0])
		oid = oid + '.' + prim_index + '.' +  second_index
		responseAddrType = snmpwalk(oid, self._rAddress, self._cString)
		oid = ''
		addrType =  self._getValueFromResponse(responseAddrType)
		#IPv4 address
		if addrType == '1':
			oid = string_to_OID(oidList[1])
		#IPv6 address
		elif addrType == '2':
			oid = string_to_OID(oidList[2])

		oid = oid + '.' + prim_index + '.' +  second_index
		responseHop = snmpwalk(oid, self._rAddress, self._cString)
		oid = ''
		#IPv4 address
		if addrType == '1':
			oid = string_to_OID(oidList[3])
		#IPv6 address
		elif addrType == '2':
			oid = string_to_OID(oidList[4])
		oid = oid + '.' + prim_index + '.' +  second_index
		responsePrefix = snmpwalk(oid, self._rAddress, self._cString)
		while addrType != None:
			singleHop =  self._getValueFromResponse(responseHop)
			addrPrefix =  self._getValueFromResponse(responsePrefix)
			if singleHop == None or addrPrefix == None:
				continue
			#TODO: what if in case of IPv6 addresses?
			hops.append(str(IPv4Address(int(singleHop,0))) + '/' + str(addrPrefix))
			addrType =  self._getValueFromResponse(responseAddrType)
		return hops
			
	def _getTunnelPaths(self):
		#For each configured tunnel
		for index in self._NameIdMap.keys():
			#Get the primary index from OID: mplsTunnelHopTableIndex
			oid = string_to_OID("mplsTunnelHopTableIndex")
			oid += '.' + index
			walk = snmpwalk(oid, self._rAddress, self._cString)
			primaryIndex = self._getValueFromResponse(walk)
			if primaryIndex == None:
				print "Error in getting the mplsTunnelHopTableIndex"
				return
			#Get the secondary index from OID: mplsTunnelPathInUse
			oid = string_to_OID("mplsTunnelPathInUse")
			oid += '.' + index
			walk = snmpwalk(oid, self._rAddress, self._cString)
			secondaryIndex = self._getValueFromResponse(walk)
			if secondaryIndex == None:
				print "Error in getting the mplsTunnelPathInUse"
				return
			#Use the two indexes to retrieve the path of the given tunnel
			path = self._getConfiguredPath(primaryIndex, secondaryIndex, "mplsTunnelHopTable")
			tunnelName = self._NameIdMap[index]
			self._ConfiguredTunnels[tunnelName].addInfo("Path", path)
			#Get also the number of bytes that traversed the tunnel
			oid = string_to_OID("mplsTunnelPerfHCBytes")
			oid += '.' + index
			walk = snmpwalk(oid, self._rAddress, self._cString)
			countBytes = self._getValueFromResponse(walk)
			if primaryIndex == None:
				print "Error in getting the mplsTunnelPerfHCBytes"
				return
			self._ConfiguredTunnels[tunnelName].addInfo("In/Out bytes", countBytes)
	
	def _getComputedPaths(self, index):
		#Get the primary index from OID: mplsTunnelCHopTableIndex
		oid = string_to_OID("mplsTunnelCHopTableIndex")
		oid += '.' + index
		walk = snmpwalk(oid, self._rAddress, self._cString)
		primaryIndex = self._getValueFromResponse(walk)
		if primaryIndex == None:
			print "Error in getting the mplsTunnelCHopTableIndex"
			return
		#There isn't a secondary index, so set it to empty char
		secondaryIndex = ''
		#Use the two indexes to retrieve the computed path of the given LSP
		path = self._getConfiguredPath(primaryIndex, secondaryIndex, "mplsTunnelCHopTable")
		tunnelDescr = self._LspIdMap[index]
		self._LspTable[tunnelDescr].addInfo("Computed Path", path)
	
	def _getResources(self, index):
		oidList = ["mplsTunnelResourceMaxRate", "mplsTunnelResourceMeanRate", "mplsTunnelResourceMaxBurstSize"]
		#Get the primary index from OID: mplsTunnelCHopTableIndex
		oid = string_to_OID("mplsTunnelResourcePointer")
		oid += '.' + index
		walk = snmpwalk(oid, self._rAddress, self._cString)
		#The return value will be like this "iso.3.6.1.3.95.2.6.1.2.1689455012"
		#The index is the last integer
		value = self._getValueFromResponse(walk)
		primaryIndex = value.split('.')[-1]
		#Now it can get the informations from the mplsTunnelResourceTable
		for oidString in oidList:
			oid = string_to_OID(oidString)
			oid += '.' + primaryIndex

			get = snmpget(oid, self._rAddress, self._cString)
			value = get[0][1]

			tunnelDescr = self._LspIdMap[index]
			self._LspTable[tunnelDescr].addInfo(oidString, value)
	
	def _getLspInfos(self, index):
		infoVect = ["mplsTunnelSetupPrio", "mplsTunnelHoldingPrio", "mplsTunnelRole", "mplsTunnelAdminStatus", "mplsTunnelOperStatus", "mplsTunnelPerfHCBytes"]
		for oidString in infoVect:
			oid = string_to_OID(oidString)
			oid += '.' + index
			#get = snmpget(oid, self._rAddress, self._cString)
			#value = get[0][1]
			walk = snmpwalk(oid, self._rAddress, self._cString)
			value = self._getValueFromResponse(walk)
			tunnelDescr = self._LspIdMap[index]
			self._LspTable[tunnelDescr].addInfo(oidString, value)
		
	def _populateLspTable(self):
		for index in self._LspIdMap.keys():
			#Get the additional informations from the mplsTunnelTable
			self._getLspInfos(index)
			#Get and insert the computed path
			self._getComputedPaths(index)
			#Get and insert the reserved resources
			self._getResources(index)
	
