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
		centerWindow(self)
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
		#If the user press "Enter" go to the next window
		ipAddressEntry.bind("<KeyPress-Return>", lambda event: self._startCmd())
		#Set the 2nd row
		snmpLabel = Label (self._labelframe, text = "SNMP community name:")
		snmpLabel.grid(column = 0, row = 1, sticky = W+N+S)
		self._snmpCommunity = StringVar()
		snmpCommunityEntry = Entry(self._labelframe, textvariable = self._snmpCommunity)
		snmpCommunityEntry.grid(padx = 5, column = 1, row = 1)
		#If the user press "Enter" go to the next window
		snmpCommunityEntry.bind("<KeyPress-Return>", lambda event: self._startCmd())
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
		centerWindow(self,900, 600)
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
		#TODO: show the network topology in the "topologyFrame"
		
		
	def _refresh(self):
		#TODO: call the right manager's function with correct parameters 
		#RefToManager.getGraph()
		return
	def _settings(self):
		#It creates a new little window where there will be the settable parameters
		self._settingsFrame = Tk()
		self._settingsFrame.title("Settings")
		setGridWeight(self._settingsFrame, 3, 2)
		centerWindow(self._settingsFrame, 400, 200)
		self._settingsFrame.grid()
		#Show two radio buttons to let the user decide the working mode: Synchronous or not
		#TODO: qui ogni volta la variabile viene ricreata, andrebbe creata una volta 
		self._pollingVar = IntVar()
		pollingButton = Radiobutton(self._settingsFrame, text = "Synchronous mode", value = 1, variable = self._pollingVar)
		noPollingButton = Radiobutton(self._settingsFrame, text = "Asynchronous mode", value = 0, variable = self._pollingVar)
		pollingButton.grid(column = 0, row = 0, sticky = W)
		noPollingButton.grid(column = 1, row = 0, sticky = E)
		#Show the field to set the refresh time
		refreshLabel = Label (self._settingsFrame, text = "Refresh time:")
		refreshLabel.grid(column = 0, row = 1, sticky = W+N+S)
		self._refreshTime = DoubleVar()
		refreshEntry = Entry(self._settingsFrame, textvariable = self._refreshTime)
		refreshEntry.grid(column = 1, row = 1)
		#If the user press Enter, close the window
		pollingButton.bind("<KeyPress-Return>", lambda event: self._closeSettings())
		noPollingButton.bind("<KeyPress-Return>", lambda event: self._closeSettings())
		refreshEntry.bind("<KeyPress-Return>", lambda event: self._closeSettings())
		return
	
	def _closeSettings(self):
		print self._pollingVar.get(),self._refreshTime.get()
		self._settingsFrame.destroy()
	
	def _links(self):
		return
	def _tunnels(self):
		return
#FOR TESTING		
def main():
	t = TeGUI(None)
	
main()
	
 		
