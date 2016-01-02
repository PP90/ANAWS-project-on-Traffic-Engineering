##Class router
##This class contains info about the router. 

from if_res import if_res

class router:
	hostname="" #Hostname of router
	address="" #Router address
	interfaces=[] #Which interfaces it has. The interface is itself an object. An apposite class has been written
	old_timeUp=-1
	new_timeUp=-1
	def __init__(self,hostname, address, interfaces):
		self.hostname=hostname
		self.address=address
		self.interfaces=interfaces

	#to print function
	def display_info(self):
		print "Hostname: ",self.hostname
		print "Address: ", self.address
		print "Time up: ",self.old_timeUp
		for x in self.interfaces:
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


	##A new byte in and out valuesare set and then is compute the difference between old and new in out bytes
	def get_inout_bytes_diff(self,in_byte, out_byte,index_if):
		in_diff, out_diff=self.interfaces[index_if].set_new_inout_byte(in_byte, out_byte)
		return in_diff, out_diff		 
	
	def add_if(self, new_iterface):
		interfaces.append(new_iterface)

	def get_hostname(self):
		return self.hostname

	def get_interfaces(self):
		return self.interfaces

	def get_interface(self, index):
		return self.interfaces[index]

	def get_address(self):
		return self.address

	def get_ifs_info(self):
		name_list=[]
		speed_list=[]
		for interface in self.interfaces:
			name_list.append(interface.get_name())
			speed_list.append(interface.get_if_speed())
		return name_list, speed_list




