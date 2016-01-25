from Tkinter import *
import tkFont
from GuiUtilities import *
from ttk import * 
import netaddr
import tkMessageBox
#from Manager.SNMP_utilization_src import getRouterInfo 
#from Manager.SNMP_utilization_src.if_res import *
#from Manager.SNMP_utilization_src.router import *
from Manager.manager import *

class TeGUI(Frame):
	def __init__(self):
		Frame.__init__(self)
		self._RefToManager = None
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
		#The tree-view that is shown inside the main window
		self._tree = None
		#State variable that specifies which kind of information is currently shown in the main window ("Topology", "Utilizations", "Tunnels")
		self._currentView = ''
		#State variable that specifies if the user wants to see all the router interface or only those that have an ip address
		self._allInterfaces = 0
		self._interfacesVar = IntVar()
		self._interfacesVar.set(self._allInterfaces)
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
		
		#Everything should be ok, create the manager object
		self._RefToManage = Manager(self._ipAddress.get(), self._snmpCommunity.get())
		
		#Clean the window up
		self._title.grid_forget()
		self._labelframe.grid_forget()
		
		#TODO: put here some label message for the user, like "Please wait" or something better
		
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
		self.infoFrame = createFrame(self, 1,1,True, "Text information")
		self.infoFrame.grid(padx = 10, pady = 10, column = 0, row = 0, sticky = W+E+S+N)
		#Create the LabelFrame that will contain command button
		commandFrame = createFrame(self, 5,1,True, "Commands")
		commandFrame.grid(padx = 10, pady = 10, column = 1, row = 0, sticky = W+E+S+N)
		#Fill the command frame with buttons
		#REFRESH
		refreshButton = Button(commandFrame, text = "Refresh information", command = self._refresh)
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
		
		#Show the topology information (This process can take a while)
		self._printTopologyInfo()
	
	def _printTopologyInfo(self, refresh = True):
		if self._tree is not None:
			self._tree.destroy()
		if refresh == True:		
			#Obtain the network topology
			self._routerAddrList = self._RefToManage.getListIP()
			self._topologyMatrix = self._RefToManage.getTopology()
			self._routerList = self._RefToManage.getRoutersList(self._routerAddrList)
		
		self._tree = createTreeView(self.infoFrame, ["Router Name", "IP address","Subnet mask","Connected to"], self._routerList, self._topologyMatrix, self._allInterfaces)
		self._tree.grid(padx = 5,pady = 5, column = 0, row = 0, sticky = W+E+S+N) 
		self._currentView = 'Topology'
	
	def _printUtilizationInfo(self):
		return
		
	def _refresh(self):
		#It must check the state variable in order to understand which function has to call
		if self._currentView == 'Topology':
			self._printTopologyInfo()
		elif self._currentView == 'Utilizations':
			self._printUtilizationInfo()
			return
		else:
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
		entriesFrame = createFrame(self._settingsFrame, 2, 2, True, "Parameters")
		entriesFrame.grid(padx = 10, pady = 10,column = 0, row = 1, columnspan = 2, sticky = W+E+S+N)
		#Show the field to set the refresh time
		refreshLabel = Label (entriesFrame, text = "Refresh time:")
		refreshLabel.grid(column = 0, row = 0)
		refreshEntry = Entry(entriesFrame, textvariable = self._refreshTimeVar)
		refreshEntry.grid(column = 1, row = 0)
		#Show two radio buttons to let the user decide if he wants to see all the interfaces or not
		interfaceButton = Radiobutton(entriesFrame, text="Show all interfaces", variable=self._interfacesVar,value=1)
		noInterfaceButton = Radiobutton(entriesFrame, text="Show only active interfaces", variable=self._interfacesVar, value=0)
		interfaceButton.grid(column = 0, row = 1)
		noInterfaceButton.grid(column = 1, row = 1)
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
		self._interfacesVar.set(self._allInterfaces)
		#Close the window
		self._settingsFrame.destroy()
		
	def _closeSettings(self):
		#FOR TESTING
		print self._pollingVar.get(),str(self._refreshTimeVar.get()), self._interfacesVar.get()
		#Check for negative time
		if self._refreshTimeVar.get() <= 0:
			self._refreshTimeVar.set(self._defaultRefreshTime)	
		#Copy the state variables in the data variables
		self._RefreshTime = self._refreshTimeVar.get()
		self._Mode = self._pollingVar.get()
		#If the user has decided to see all or only active interfaces
		if self._allInterfaces != self._interfacesVar.get():
			self._allInterfaces = self._interfacesVar.get()
			self._printTopologyInfo(False)
		else:
			self._allInterfaces = self._interfacesVar.get()
		#Close the window
		self._settingsFrame.destroy()
	
	def _links(self):
		return
	def _tunnels(self):
		return
	def _topology(self):
		self._printTopologyInfo()
		self._currentView = 'Topology'
#FOR TESTING		
def main():
	t = TeGUI()
	
main()
	
 		
