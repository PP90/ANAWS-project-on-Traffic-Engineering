##Class router
##This class contains info about the router. 

from if_res import if_res

class router:
	hostname="" #Hostname of router
	address="" #Router address
	interfaces=[] #Which interfaces it has. The interface is itself an object. An apposite class has been written

	def __init__(self,hostname, address, interfaces):
		self.hostname=hostname
		self.address=address
		self.interfaces=interfaces

	#to print function
	def display_info(self):
		print "Hostname: ",self.hostname
		print "Address: ", self.address
		for x in self.interfaces:
			x.display_info()

	def set_hostname(self):
		self.hostname=hostname
		
	def set_in_bytes_to_if(self, in_byte, index_if):
		self.interfaces[index_if].set_old_in_byte(in_byte)

	def set_out_bytes_to_if(self, out_byte, index_if):
		self.interfaces[index_if].set_old_out_byte(out_byte)
	
	def add_if(self, new_iterface):
		interfaces.append(new_iterface)

	def get_hostname(self):
		return self.hostname

	def get_interfaces(self):
		return self.interfaces

	def get_interface(self, index):
		return self.interfaces[index]
