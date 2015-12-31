##Class if_res.
##This class contains info about the interface. if_res meaning is interface resource.
##
class if_res:
	id_if=-1##Id interface
	name=""##Name of interface
	speed=-1##speed of interface

	old_ifInBytes=0 ##old values of in and output bytes
	old_ifOutBytes=0

	old_timeUp=0;##old values of in and output bytes

	new_ifInBytes=0 ####new values of in and output bytes
	new_ifOutBytes=0
	
	def __init__(self, id_if, name, speed):
		self.id_if=id_if
		self.name=name
		self.speed=speed

	#to print function
	def display_info(self):
		print 'ID:', self.id_if, 'Interface: ', self.name, ' Speed: ', self.speed, ' bit\sec', 'IN bytes: ', self.old_ifInBytes, 'OUT bytes: ', self.old_ifOutBytes
	def set_id_if(self):
		self.id_if=id_if

	def set_name_if(self):
		self.name=name

	def set_name_if(self):
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
		print self.name	
		return in_byte_diff,out_byte_diff
	

	def set_old_timeUp(self, old_timeUp):
		self.old_timeUp=old_timeUp;

	def get_old_in_byte(self):
		return self.old_ifInBytes

	def get_old_out_byte(self):
		return self.old_ifOutBytes


