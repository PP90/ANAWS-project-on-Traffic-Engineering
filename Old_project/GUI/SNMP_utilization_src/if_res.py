##Class if_res.
##This class contains info about the interface. if_res meaning is interface resource.
##
class if_res:
	id_if=-1##Id interface
	name=""##Name of interface
	speed=-1##speed of interface
	ipAddress=''	#Ipv4 or IPv6 interface address
	subnetMask = '' #Subnet mask

	old_ifInBytes=0 ##old values of in and output bytes
	old_ifOutBytes=0

	new_ifInBytes=0 ####new values of in and output bytes
	new_ifOutBytes=0
	
	in_utilization=0
	out_utilization=0

	def __init__(self, id_if, name, speed, ipAddress=None):
		self.id_if=id_if
		self.name=name
		self.speed=speed
		self.ipAddress = ipAddress

	#to print function
	def display_info(self):
		print 'ID:', self.id_if, 'Interface: ', self.name, ' Speed: ', self.speed, ' bit\sec', 'IN bytes: ', self.old_ifInBytes, 'OUT bytes: ', self.old_ifOutBytes, ' IP address: ', self.ipAddress
		
	def set_address_if(self, address):
		self.ipAddress = address
	
	def get_address_if(self):
		return self.ipAddress
		
	def set_subnet_if(self, subnet):
		self.subnetMask = subnet
		
	def get_subnet_if(self):
		return(self.subnetMask)
	
	def set_id_if(self, id_if):
		self.id_if=id_if

	def set_name_if(self, name):
		self.name=name

	def set_speed_if(self, speed):
		self.speed=speed

	def get_id(self):
		return self.id_if

	def get_if_speed(self):
		return self.speed

	def get_name(self):
		return self.name

	def get_old_timeUp(self):
		return self.old_timeUp;

	def set_old_in_byte(self, old_ifInBytes):
		self.old_ifInBytes=old_ifInBytes
	
	def set_old_out_byte(self, old_ifOutBytes):
		self.old_ifOutBytes=old_ifOutBytes

	def set_new_inout_byte(self, new_ifInBytes, new_ifOutBytes):
		self.old_ifInBytes=self.new_ifInBytes
		self.new_ifInBytes=new_ifInBytes

		self.old_ifOutBytes=self.new_ifOutBytes		
		self.new_ifOutBytes=new_ifOutBytes
		
		in_byte_diff=self.new_ifInBytes-self.old_ifInBytes
		out_byte_diff=self.new_ifOutBytes-self.old_ifOutBytes
		return in_byte_diff,out_byte_diff
	

	def set_old_timeUp(self, old_timeUp):
		self.old_timeUp=old_timeUp;

	def set_in_out_utilization(self, in_uti, out_uti):
		self.in_utilization=in_uti
		self.out_utilization=out_uti

	def get_old_in_byte(self):
		return self.old_ifInBytes

	def get_old_out_byte(self):
		return self.old_ifOutBytes

	def get_in_out_utilization(self):
		return self.in_utilization, self.out_utilization


