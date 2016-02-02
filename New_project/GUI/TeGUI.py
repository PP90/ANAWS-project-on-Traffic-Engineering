from Tkinter import *
import tkFont
from GuiUtilities import *
from ttk import * 
import netaddr
import tkMessageBox
from Manager.Mpls_snmp.Container import * 
from Manager.manager import *
from threading import *

class TeGUI(Frame):
	def __init__(self):
		Frame.__init__(self)
		self.master.protocol("WM_DELETE_WINDOW", self.closeGUI)
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
		#State variable that specifies if the topology is retrieved through Quagga ('Q') or Telnet ('T')
		self._QuaggaOrTelnet = StringVar()
		self._QuaggaOrTelnet.set('T')
		#The tree-view that is shown inside the main window
		self._tree = None
		#State variable that specifies which kind of information is currently shown in the main window ("Topology", "Utilizations", "Tunnels")
		self._currentView = ''
		#State variable that specifies if the user wants to see all the router interface or only those that have an ip address
		self._allInterfaces = 0
		self._interfacesVar = IntVar()
		self._interfacesVar.set(self._allInterfaces)
		#Item selected in the tree-view
		self._itemSelected = ''
		#List of router address which tunnels are shown in the window
		self._shownTunnels = []
		#Tree-view reserved for tunnels
		self._underTree = None
		#Create the condition object for implementing the lock
		self.lock = Condition()
		#The graph object to show to the user
		self._graph = None
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
		if self._graph != None:
			self._graph.close()
		if self._RefToManager != None:
			self._RefToManager.stopThreads()
		self.master.destroy()
	def setUtilization(self, utilizations):
		#Must be thread safe
		self.lock.acquire()
		if self._currentView == "Utilizations":
			utilizTreeView(self._tree, ["Router Name", "Speed","Utilization %","Connected to"], utilizations)
		self.lock.release()
			
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
		self._labelframe = createFrame(self, 4, 2, True)
		self._labelframe.grid(padx = 10, pady = 10,row = 1, column= 0,sticky = W+E+N+S)
		
		#Set the 1st row 
		addressLabel = Label (self._labelframe, text = "Router IP address:")
		addressLabel.grid(column = 0, row = 0, sticky = W+N+S)
		
		self._ipAddressEntry = Entry(self._labelframe, textvariable = self._ipAddress, justify=CENTER)
		self._ipAddressEntry.grid(padx = 5,column = 1, row = 0)
		#If the user press "Enter" go to the next window
		self._ipAddressEntry.bind("<KeyPress-Return>", lambda event: self._startCmd())
		#Set the 2nd row
		snmpLabel = Label (self._labelframe, text = "SNMP community name:")
		snmpLabel.grid(column = 0, row = 1, sticky = W+N+S)
		
		snmpCommunityEntry = Entry(self._labelframe, textvariable = self._snmpCommunity, justify=CENTER)
		snmpCommunityEntry.grid(padx = 5, column = 1, row = 1)
		#If the user press "Enter" go to the next window
		snmpCommunityEntry.bind("<KeyPress-Return>", lambda event: self._startCmd())
		
		#Set the 3rd row
		topologyLabel = Label (self._labelframe, text = "Retrieve network topology using:")
		topologyLabel.grid(column = 0, row = 2, columnspan = 1,sticky = W)
		telnetButton = Radiobutton(self._labelframe, text="Telnet", variable=self._QuaggaOrTelnet,value='T', command = self._selectQuagga)
		quaggaButton = Radiobutton(self._labelframe, text="Quagga", variable=self._QuaggaOrTelnet, value='Q', command = self._selectQuagga)
		telnetButton.grid(column = 1, row = 2, sticky = W, padx = 10)
		quaggaButton.grid(column = 1, row = 2, sticky = E, padx = 10)
		
		#Set the 4rd row
		startButton = Button(self._labelframe, text = "Start", command = self._startCmd)
		startButton.grid(padx = 5, column = 1, row = 3) 
		
		
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
		if self._QuaggaOrTelnet.get() == 'T':
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
		self._RefToManager = Manager(self._ipAddress.get(), self._snmpCommunity.get(), self._QuaggaOrTelnet.get(), self)
		
		#Clean the window up
		self._title.grid_forget()
		self._labelframe.grid_forget()
		
		#TODO: put here some label message for the user, like "Please wait" or something better
		
		#Create the new window
		self._createMainWindow()
		return
		
	def _selectQuagga(self):
		if self._QuaggaOrTelnet.get() == 'Q':
			if self._ipAddress.get() == '':
				self._ipAddress.set("Disabled")
       			self._ipAddressEntry.configure(state='disabled')
   		else:
   			if self._ipAddress.get() == 'Disabled':
				self._ipAddress.set("")
        		self._ipAddressEntry.configure(state='normal')
	
	def _createMainWindow(self):
		centerWindow(self,1000, 700)
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
		linkButton = Button(commandFrame, text = "Show link utilization", command = self._links)
		linkButton.grid(padx = 5, column = 0, row = 2) 
		#TUNNELS
		tunnelsButton = Button(commandFrame, text = "Show TE tunnels", command = self._tunnels)
		tunnelsButton.grid(padx = 5, column = 0, row = 3) 
		#TOPOLOGY
		tunnelsButton = Button(commandFrame, text = "Show network topology", command = self._topology)
		tunnelsButton.grid(padx = 5, column = 0, row = 4) 
		
		#Show the topology information (This process can take a while)
		self._printTopologyInfo()
		self._currentView = 'Topology'
	
	def _printTopologyInfo(self, refresh = True):
		if self._tree is not None:
			self._tree.destroy()
		if refresh == True:		
			#Obtain the network topology
			self._routerAddrList = self._RefToManager.getListIP()
			self._topologyMatrix = self._RefToManager.getTopology()
			self._routerList = self._RefToManager.getRoutersList(self._routerAddrList)
			self._routerAddrList.pop(self._routerAddrList.index("192.168.0.100"))
		
		self._tree = createTreeView(self.infoFrame, ["Router Name", "IP address","Subnet mask","Connected to"], self._routerList, self._topologyMatrix, self._allInterfaces)
		self._tree.grid(padx = 5,pady = 5, column = 0, row = 0, sticky = W+E+S+N) 
		self._tree.bind('<ButtonRelease-1>', self._selectTreeItem)
		#Show the graph describing the network topology
		self._graph = self._RefToManager.getGraph(self._topologyMatrix)
		self._graph.show()
	
	def _selectTreeItem(self, event):
		self._itemSelected = getItemSelected(self._tree)
				
	
	def _printUtilizationInfo(self, refresh = False):
		#Obtain all utilization from each router
		response = {}
		response = self._RefToManager.getAllUtilization(self._routerAddrList, refresh)
		self._tree = utilizTreeView(self._tree, ["Router Name", "Speed","Utilization %","Connected to"], response)
		self._tree.grid(padx = 5,pady = 5, column = 0, row = 0, sticky = W+E+S+N)
		#Start the thread for the polling if the mode is setted to async
		if self._Mode == 0:
			self._RefToManager.startThreads(self._RefreshTime, self._routerAddrList) 
		 
	
	def _printTunnelsInfo(self):
		response = {}
		routerAddr = ''
		routerObj = None
		#If the tunnels relative to this router are alreaty shown
		if self._itemSelected in self._shownTunnels:
			return
		
		#In self._itemSelected there is the name of the selected router, but we need its ip address
		for router in self._routerList:
			if router.get_hostname() == self._itemSelected:
				routerAddr = router.get_address()
				routerObj = router
		if routerAddr == '':
			self.sendAlertMsg("Error: Host name " + self._itemSelected + " not found")
			return
			
		self._shownTunnels.append(self._itemSelected)
		response = self._RefToManager.getAllTunnels(routerAddr)
		formattedPaths = self._RefToManager.getTunnel(routerAddr)
		#Filter the tunnels information
		for tunnel in response.keys():
			role = response[tunnel].getAttribute('mplsTunnelRole')
			if role != '1':
				response.pop(tunnel) #tunnel that doesn't start from that router->remove this entry
			else:
				#Translate the path into a list of router name from a list of routers' ip addresses
				path = response[tunnel].getAttribute('Computed Path')
				formattedPath = formattedPaths[tunnel]
				for hop in formattedPath:
					for router in self._routerList:
						if router.get_address() == hop:
							formattedPath[formattedPath.index(hop)] = router.get_hostname()
							break
				response[tunnel].setAttribute('Computed Path',formattedPath)
		#If the tunnel tree is not already created
		if self._underTree == None:		
			self._underTree = createTunnelsTree(self.infoFrame, ["Name", "Source","Destination","Path","Max rate", "Max burst", "Mean rate"] , response, routerObj)
			setGridWeight(self.infoFrame, 2, 1)
			self._underTree.grid(padx = 5,pady = 5, column = 0, row = 1, sticky = W+E+S+N) 
			self._tree.grid(padx = 5,pady = 5, column = 0, row = 0, sticky = W+E+S+N) 
		else:
			addTunnel(self._underTree, response, routerObj)
		
	def _refresh(self):
		#It must check the state variable in order to understand which function has to call
		if self._currentView == 'Topology':
			self._printTopologyInfo()
		elif self._currentView == 'Utilizations':
			self._printUtilizationInfo(True)
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
		#Check if the refresh time is changed 
		if self._RefreshTime != self._refreshTimeVar.get() and self._currentView == 'Utilizations':
			#Restart the threads with the new time interval
			self._RefToManager.stopThreads()
			self._RefToManager.startThreads(self._refreshTimeVar.get(), self._routerAddrList)
		self._RefreshTime = self._refreshTimeVar.get()
		#Check if the working mode is changed
		if self._Mode != self._pollingVar.get() and self._currentView == 'Utilizations':
			#If equal to 0 async mode, otherwise sync. Default = 1
			if self._pollingVar.get() == 0:
				self._RefToManager.startThreads(self._refreshTimeVar.get(), self._routerAddrList)
			else:
				self._RefToManager.stopThreads()
		self._Mode = self._pollingVar.get()
		#If the user has decided to see all or only active interfaces
		if self._allInterfaces != self._interfacesVar.get() and self._currentView == 'Topology':
			self._allInterfaces = self._interfacesVar.get()
			self._printTopologyInfo(False)
		else:
			self._allInterfaces = self._interfacesVar.get()
		#Close the window
		self._settingsFrame.destroy()
	
	def _links(self):
		if self._currentView == 'Utilizations':
			return
		self._currentView = 'Utilizations'
		self._printUtilizationInfo()
	def _tunnels(self):
		if self._itemSelected == '':
			self.sendAlertMsg("Please select a router in the list")
			return
		msg = "You have selected router " + self._itemSelected +". Continue?"
		selectItem(self._tree,self._itemSelected)
		response = tkMessageBox.askyesno(title = "Retrieve tunnels", message = msg, parent = self)
		if response == True:
			self._printTunnelsInfo()
			
	def _topology(self):
		if self._currentView == 'Topology':
			return
		self._printTopologyInfo()
		self._currentView = 'Topology'
#FOR TESTING		
def main():
	t = TeGUI()
	
main()
	
 		
