from Tkinter import *
import tkFont
from GuiUtilities import *
from ttk import * 
import netaddr
import tkMessageBox

class TeGUI(Frame):
	def __init__(self, RefToManager):
		
		self._startGUI()
	
	def setTopologyImg(self, imgPath, infoFlag):
		return
	def setRouterList(self, RouterObjectList):
		return
	def sendAlertMsg(self, stringMsg):
		tkMessageBox.showwarning(title = "Warning!", message = stringMsg, parent = self)
		return
	def setTunnelList(self, routerName ,TunnelObjectList):
		return
	def closeGUI(self):
		return
	"""This function creates the user interface with the first layout"""
	def _startGUI(self):
		Frame.__init__(self)
		#Set the window title
		self.master.title("TE Dashboard")
		#Set the window size
		self.master.geometry("600x400")
		self.master.rowconfigure(0, weight=1)
		self.master.columnconfigure(0, weight=1)
		self.grid(sticky = W+E+N+S)
		#Set the style
		self.style = Style()
		self.style.theme_use("clam")
		
		#Set the number of grid columns and rows of the window, for the moment we need 2 rows and 1 column
		setGridWeight(self, 2, 1)
            	
            	#Set the first label string
		self._titleFont = tkFont.Font(family = "Verdana", size = 16, weight = "bold")
		self._title = Label (self, font = self._titleFont, text = "Traffic Engineering Dashboard")
		self._title.grid(column = 0, row = 0)
            		
		#Set the LabelFrame that will contain the form
		labelframe = createFrame(self, 3, 2, 1)
		labelframe.grid(padx = 10, pady = 10,row = 1, column= 0,sticky = W+E+N+S)
		
		#Set the 1st row 
		addressLabel = Label (labelframe, text = "Router IP address:")
		addressLabel.grid(column = 0, row = 0, sticky = W+N+S)
		self._ipAddress = StringVar()
		ipAddressEntry = Entry(labelframe, textvariable = self._ipAddress)
		ipAddressEntry.grid(padx = 5,column = 1, row = 0)
		#Set the 2nd row
		snmpLabel = Label (labelframe, text = "SNMP community name:")
		snmpLabel.grid(column = 0, row = 1, sticky = W+N+S)
		self._snmpCommunity = StringVar()
		snmpCommunityEntry = Entry(labelframe, textvariable = self._snmpCommunity)
		snmpCommunityEntry.grid(padx = 5, column = 1, row = 1)
		#Set the 3rd row
		startButton = Button(labelframe, text = "Start", command = self._startCmd)
		startButton.grid(padx = 5, column = 1, row = 2) 
		
		#create the GUI main loop
		self.mainloop()
	
	def _startCmd(self):
		#When the start button is pressed we need to check the inputs values
		alertMsg = ""
		#Check the SNMP community name
		if self._snmpCommunity.get() == "":
			alertMsg += "Community name is empty\n"
		else:
			self._snmpCommunityName = self._snmpCommunity.get()
		#Check the router IP address (note that it may be IPv4 or IPv6 address)
		temp = self._ipAddress.get()
		try:
			self._routerIpAddr = netaddr.IPAddress(temp)
		except netaddr.AddrFormatError:
			alertMsg += "Router IP address is not valid\n"
			
		#If the alertMsg is not empty it means that something went wrong
		if alertMsg != "":
			self.sendAlertMsg(alertMsg)
			return
		
		return

#FOR TESTING		
def main():
	t = TeGUI(None)
	
main()
	
 		
