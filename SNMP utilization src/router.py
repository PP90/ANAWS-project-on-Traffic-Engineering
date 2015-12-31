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

	def get_timeUp_diff(self, timeUp):
		
		self.old_timeUp=self.new_timeUp
		self.new_timeUp=timeUp
		diff_timeUp=self.new_timeUp-self.old_timeUp
		return diff_timeUp

	def set_hostname(self):
		self.hostname=hostname

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

	def get_ifs_info(self):
		name_list=[]
		speed_list=[]
		for interface in self.interfaces:
			name_list.append(interface.get_name())
			speed_list.append(interface.get_if_speed())
		return name_list, speed_list




