from Tkinter import *
import tkFont
from GuiUtilities import *
from ttk import * 
import netaddr
import tkMessageBox

class TeGUI(Frame):
	def __init__(self, RefToManager):
		#TODO: check for None parameter
		self._RefToManager = RefToManager
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
		self._centerWindow()
		self.master.rowconfigure(0, weight=1)
		self.master.columnconfigure(0, weight=1)
		self.grid(sticky = W+E+N+S)
		#Set the style
		self.style = Style()
		self.style.theme_use("clam")
		
		#Set the number of grid columns and rows of the window, for the moment we need 2 rows and 1 column
		setGridWeight(self, 2, 1)
            	
            	#Set the first label string
		titleFont = tkFont.Font(family = "Verdana", size = 16, weight = "bold")
		self._title = Label (self, font = titleFont, text = "Traffic Engineering Dashboard")
		self._title.grid(column = 0, row = 0)
            		
		#Set the LabelFrame that will contain the form
		self._labelframe = createFrame(self, 3, 2, True)
		self._labelframe.grid(padx = 10, pady = 10,row = 1, column= 0,sticky = W+E+N+S)
		
		#Set the 1st row 
		addressLabel = Label (self._labelframe, text = "Router IP address:")
		addressLabel.grid(column = 0, row = 0, sticky = W+N+S)
		self._ipAddress = StringVar()
		ipAddressEntry = Entry(self._labelframe, textvariable = self._ipAddress)
		ipAddressEntry.grid(padx = 5,column = 1, row = 0)
		#Set the 2nd row
		snmpLabel = Label (self._labelframe, text = "SNMP community name:")
		snmpLabel.grid(column = 0, row = 1, sticky = W+N+S)
		self._snmpCommunity = StringVar()
		snmpCommunityEntry = Entry(self._labelframe, textvariable = self._snmpCommunity)
		snmpCommunityEntry.grid(padx = 5, column = 1, row = 1)
		#Set the 3rd row
		startButton = Button(self._labelframe, text = "Start", command = self._startCmd)
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
		
		#Everything should be ok, retrieve the network topology
		#TODO: call the right manager's function with correct parameters 
		#RefToManager.getGraph()
		
		#Clean the window up
		self._title.grid_forget()
		self._labelframe.grid_forget()
		
		#Create the new window
		self._createMainWindow()
		return
		
	def _createMainWindow(self):
		self._centerWindow(900, 600)
		#Set the number of grid columns and rows of the window, we need 2 rows and 2 column
		setGridWeight(self, 2, 2,[5, 95],[70, 30])
		#masterFrame = createFrame(self, 2,2,0)
		#masterFrame.grid()
		#Set the 1st row with two info strings: router ip address and snmp community string
		string = "Router IP address: " + self._ipAddress.get() + "\nSNMP Community name: " + self._snmpCommunity.get()
		routerString = Label (self, text = string)
		routerString.grid(column = 0, row = 0, sticky = W)
		
		#Create the LabelFrame that will contain the topology image
		topologyFrame = createFrame(self, 1,1,True, "Network topology")
		topologyFrame.grid(padx = 10, pady = 10, column = 0, row = 1, sticky = W+E+S+N)
		#Create the LabelFrame that will contain command button
		commandFrame = createFrame(self, 5,1,True, "Commands")
		commandFrame.grid(padx = 10, pady = 10, column = 1, row = 1, sticky = W+E+S+N)
		#Fill the command frame with buttons
		#REFRESH
		refreshButton = Button(commandFrame, text = "Refresh", command = self._refresh)
		refreshButton.grid(padx = 5, column = 0, row = 0) 
		#SET PARAMETERS
		paramButton = Button(commandFrame, text = "Settings", command = self._settings)
		paramButton.grid(padx = 5, column = 0, row = 1) 
		#LINKS UTILIZATIONS
		linkButton = Button(commandFrame, text = "Links utilization", command = self._links)
		linkButton.grid(padx = 5, column = 0, row = 2) 
		#TUNNELS
		tunnelsButton = Button(commandFrame, text = "TE tunnels", command = self._tunnels)
		tunnelsButton.grid(padx = 5, column = 0, row = 3) 
		
	def _centerWindow(self, w = 600, h = 400):
		sw = self.master.winfo_screenwidth()
		sh = self.master.winfo_screenheight()
		x = (sw - w)/2
		y = (sh - h)/2
		self.master.geometry('%dx%d+%d+%d' % (w,h,x,y))
		
	def _refresh(self):
		return
	def _settings(self):
		return
	def _links(self):
		return
	def _tunnels(self):
		return
#FOR TESTING		
def main():
	t = TeGUI(None)
	
main()
	
 		
