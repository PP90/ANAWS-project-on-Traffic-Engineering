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
		
		"""First phase: get the configured tunnel names"""
		self._getTunnelName()
		"""2nd phase: get the LSP descriptive name"""
		self._getLspDescr()
		
	def _parse_oid(self, response_oid):
		"""The OID for mpls-te is composed as follows: 'resource_oid.tunnel_id.tunnel_instance.source_ip_address.destination_ip_address'"""
		resource = response_oid[:-4]
		#the ip addresses are in decimal format, so they need convertion
		dest_ip = str(IPv4Address(response_oid[-1]))
		source_ip = str(IPv4Address(response_oid[-2]))
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
				index = str(tun_id) + str(tun_instance)
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
				index = str(tun_id) + str(tun_instance)
				tunnelDescr = val.prettyPrint()
				tunnelName = self._NameIdMap[index]
				self._ConfiguredTunnels[tunnelName].addInfo("Descriptive Name", tunnelDescr)
			#Analyze the rows regarding to LSP instance
			else:
				index = str(tun_id) + str(tun_instance)
				tunnelDescr = val.prettyPrint()
				#add the mapping between "tunID.tunInst" <--> "Tunnel Descriptive Name"
				self._LspIdMap[index] = tunnelDescr
				#add an object to the dictionary "_LspTable"
				LspInstance = Container(tunnelDescr)
				self._LspTable[tunnelDescr] = LspInstance
			row = next_record(walk)
