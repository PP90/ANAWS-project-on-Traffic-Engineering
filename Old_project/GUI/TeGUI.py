from Tkinter import *
import tkFont
from GuiUtilities import *
from ttk import * 
import netaddr
import tkMessageBox
from SNMP_utilization_src import getRouterInfo 
from SNMP_utilization_src.if_res import *
from SNMP_utilization_src.router import *

class TeGUI(Frame):
	#TODO: Creare l'oggetto Manager
	def __init__(self, RefToManager):
		Frame.__init__(self)
		#TODO: check for None parameter
		self._RefToManager = RefToManager
		self._ipAddress = StringVar()
		self._snmpCommunity = StringVar()
		#Working mode: polling (synchronous)  = 1 or asynchronous = 0
		self._Mode = 1
		self._pollingVar = IntVar()
		#Set the default value equal to 1, that is the sync mode
		self._pollingVar.set(self._Mode)
		#In case of polling: refresh time is minimum interval of time between a request and another
		self._RefreshTime = 1
		self._refreshTimeVar = DoubleVar()
		#Default refresh time = 1 second
		self._defaultRefreshTime = 1
		self._refreshTimeVar.set(self._defaultRefreshTime)
		#Start the GUI
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
		
		ipAddressEntry = Entry(self._labelframe, textvariable = self._ipAddress)
		ipAddressEntry.grid(padx = 5,column = 1, row = 0)
		#If the user press "Enter" go to the next window
		ipAddressEntry.bind("<KeyPress-Return>", lambda event: self._startCmd())
		#Set the 2nd row
		snmpLabel = Label (self._labelframe, text = "SNMP community name:")
		snmpLabel.grid(column = 0, row = 1, sticky = W+N+S)
		
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
		setGridWeight(self, 1, 2,[100],[80, 20])
		#masterFrame = createFrame(self, 2,2,0)
		#masterFrame.grid()
		
		#Create the LabelFrame that will contain the topology information
		topologyFrame = createFrame(self, 1,1,True, "Text information")
		topologyFrame.grid(padx = 10, pady = 10, column = 0, row = 0, sticky = W+E+S+N)
		#Create the LabelFrame that will contain command button
		commandFrame = createFrame(self, 5,1,True, "Commands")
		commandFrame.grid(padx = 10, pady = 10, column = 1, row = 0, sticky = W+E+S+N)
		#Fill the command frame with buttons
		#REFRESH
		refreshButton = Button(commandFrame, text = "Refresh current image", command = self._refresh)
		refreshButton.grid(padx = 5, column = 0, row = 0) 
		#SET PARAMETERS
		paramButton = Button(commandFrame, text = "Settings", command = self._settings)
		paramButton.grid(padx = 5, column = 0, row = 1) 
		#LINKS UTILIZATIONS
		linkButton = Button(commandFrame, text = "Show links utilization", command = self._links)
		linkButton.grid(padx = 5, column = 0, row = 2) 
		#TUNNELS
		tunnelsButton = Button(commandFrame, text = "Show TE tunnels", command = self._tunnels)
		tunnelsButton.grid(padx = 5, column = 0, row = 3) 
		#TOPOLOGY
		tunnelsButton = Button(commandFrame, text = "Show network topology", command = self._topology)
		tunnelsButton.grid(padx = 5, column = 0, row = 4) 
		#TODO: show the network topology in the "topologyFrame"
		routerList = getRouterInfo.get_routers_list(["1.1.1.1", "2.2.2.2", "3.3.3.3", "4.4.4.4", "5.5.5.5"], "public")
		tree = createTreeView(topologyFrame, ["Router Name", "IP address","Subnet mask","Connected to"], routerList)
		tree.grid(padx = 5,pady = 5, column = 0, row = 0, sticky = W+E+S+N) 
		
		
	def _refresh(self):
		#TODO: call the right manager's function with correct parameters 
		#RefToManager.getGraph()
		return
	def _settings(self):
		#It creates a new little window where there will be the settable parameters
		self._settingsFrame = Toplevel(self)
		self._settingsFrame.title("Settings")
		setGridWeight(self._settingsFrame, 3, 2)
		centerWindow(self._settingsFrame, 400, 200)
		self._settingsFrame.grid()
		
		#Create the Label Frame for the two radio buttons
		radioFrame = createFrame(self._settingsFrame, 1, 2, True, "Working mode")
		radioFrame.grid(padx = 10, pady = 10,column = 0, row = 0, columnspan = 2, sticky = W+E+S+N)
		#Show two radio buttons to let the user decide the working mode: Synchronous or not
		pollingButton = Radiobutton(radioFrame, text="Synchronous mode", variable=self._pollingVar,value=1)
		noPollingButton = Radiobutton(radioFrame, text="Asynchronous mode", variable=self._pollingVar, value=0)
		pollingButton.grid(column = 0, row = 0)
		noPollingButton.grid(column = 1, row = 0)
		
		#Create the Label Frame for the parameters entries
		entriesFrame = createFrame(self._settingsFrame, 1, 2, True, "Parameters")
		entriesFrame.grid(padx = 10, pady = 10,column = 0, row = 1, columnspan = 2, sticky = W+E+S+N)
		#Show the field to set the refresh time
		refreshLabel = Label (entriesFrame, text = "Refresh time:")
		refreshLabel.grid(column = 0, row = 0)
		refreshEntry = Entry(entriesFrame, textvariable = self._refreshTimeVar)
		refreshEntry.grid(column = 1, row = 0)
		#Save button
		saveButton = Button(self._settingsFrame, text = "Save", command = self._closeSettings)
		saveButton.grid(column = 0, row = 2) 
		#Cancel button
		cancelButton = Button(self._settingsFrame, text = "Cancel", command = self._cancelSettings)
		cancelButton.grid(column = 1, row = 2) 
		
		#If the user press Enter, close the window
		pollingButton.bind("<KeyPress-Return>", lambda event: self._closeSettings())
		noPollingButton.bind("<KeyPress-Return>", lambda event: self._closeSettings())
		refreshEntry.bind("<KeyPress-Return>", lambda event: self._closeSettings())
		
		return
	
	def _cancelSettings(self):
		#Restore the state variables to the previous values
		self._refreshTimeVar.set(self._RefreshTime)
		self._pollingVar.set(self._Mode)
		#Close the window
		self._settingsFrame.destroy()
		
	def _closeSettings(self):
		#FOR TESTING
		print self._pollingVar.get(),str(self._refreshTimeVar.get())
		#Check for negative time
		if self._refreshTimeVar.get() <= 0:
			self._refreshTimeVar.set(self._defaultRefreshTime)	
		#Copy the state variables in the data variables
		self._RefreshTime = self._refreshTimeVar.get()
		self._Mode = self._pollingVar.get()
		#Close the window
		self._settingsFrame.destroy()
	
	def _links(self):
		return
	def _tunnels(self):
		return
	def _topology(self):
		return
#FOR TESTING		
def main():
	t = TeGUI(None)
	
main()
	
 		
