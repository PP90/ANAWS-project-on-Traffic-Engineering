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
##Class router
##This class contains info about the router. 

from if_res import if_res

class router:
	hostname="" #Hostname of router
	address="" #Router address
	interfaces = {} #Which interfaces it has. The interface is itself an object. An apposite class has been written
	old_timeUp=-1
	new_timeUp=-1		


	def __init__(self,hostname="No_name", address='0.0.0.0', interfaces={}):
		self.hostname=hostname
		self.address=address
		self.interfaces=interfaces

	#to print function
	def display_info(self):
		print "Hostname: ",self.hostname
		print "Address: ", self.address
		print "Time up: ",self.old_timeUp
		for x in list(self.interfaces.values()):
			x.display_info()
			
	##A new time up values is set and then is computed the difference between old and new timeUp
	def get_timeUp_diff(self, timeUp):
		self.old_timeUp=self.new_timeUp
		self.new_timeUp=timeUp
		diff_timeUp=self.new_timeUp-self.old_timeUp
		return diff_timeUp

	def get_old_timeUp(self):
		return self.old_timeUp

	def set_hostname(self, hostname):
		self.hostname=hostname

	def set_old_timeUp(self, old_timeUp):
		self.old_timeUp=old_timeUp

	def set_interfaces(self, interfaces):
		#Since the internal representation is a dictionary with tuple as <InterfaceId, InterfaceObj>
		#We have to convert the passed list to dictionary
		for interface in interfaces:
			self.interfaces[interface.get_id()]=interface

	##A new byte in and out valuesare set and then is compute the difference between old and new in out bytes
	def get_inout_bytes_diff(self,in_byte, out_byte,index_if):

		if(isinstance(self.interfaces, list)==True):
			print "Is a list"
			
		in_diff, out_diff=self.interfaces[index_if].set_new_inout_byte(in_byte, out_byte)
		
		return in_diff, out_diff		 
	
	def set_inout_utilization_if(self, index_if, in_uti, out_uti):
		self.interfaces[index_if].set_in_out_utilization(in_uti, out_uti)
		
	def add_if(self, new_iterface):
		interfaces.append(new_iterface)

	def get_hostname(self):
		return self.hostname

	def get_interfaces(self):
		return list(self.interfaces.values())

	def get_single_interface(self, index):
		return self.interfaces[index]

	def get_address(self):
		return self.address

	def print_ifs_utilization(self):
		print 'Router', self.hostname
		for interface in list(self.interfaces.values()):
			print 'The (in, out) utilization  of interface ',interface.get_name(), ' is ', interface.get_in_out_utilization()

	def get_ifs_info(self):
		name_list=[]
		speed_list=[]
		for interface in list(self.interfaces.values()):
			name_list.append(interface.get_name())
			speed_list.append(interface.get_if_speed())
		return name_list, speed_list




