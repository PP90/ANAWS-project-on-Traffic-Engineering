class if_res:
	id_if=-1
	name=""
	speed=-1
	old_ifInBytes=0
	old_ifOutBytes=0
	ifInBytes=0
	ifOutBytes=0
	
	def __init__(self):
		print 'Empty constructor to fill'


	def __init__(self, id_if, name, speed):
		self.id_if=id_if
		self.name=name
		self.speed=speed

	def display_info(self):
		print 'ID interface: ', self.id_if
		print 'name interface: ', self.name
		print 'speed: ', self.speed

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

	def set_old_in_byte(self, old_ifInBytes):
		self.old_ifInBytes=old_ifInBytes
	
	def set_old_out_byte(self, old_ifOutBytes):
		self.old_ifOutBytes=old_ifOutBytes

	def get_old_in_byte(self):
		return self.old_ifInBytes

	def get_old_out_byte(self):
		return self.old_ifOutBytes


