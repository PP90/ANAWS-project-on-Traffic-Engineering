from Tkinter import *
import tkFont


class TeGUI(Frame):
	def __init__(self, RefToManager):
		
		self._startGUI()
	
	def setTopologyImg(self, imgPath, infoFlag):
		return
	def setRouterList(self, RouterObjectList):
		return
	def sendAlertMsg(self, stringMsg):
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
		
		#Set the number of grid columns and rows of the window, for the moment we need 3 rows and 1 column
		for r in range(3):
            		self.rowconfigure(r, weight=1)   
        	for c in range(1):
            		self.columnconfigure(c, weight=1)
            	
            	
            	#Set the first label string
		self._titleFont = tkFont.Font(family = "Verdana", size = 16, weight = "bold")
		self._title = Label (self, font = self._titleFont, text = "Traffic Engineering Dashboard")
		self._title.grid(column = 0, row = 0,  columnspan = 2, sticky = W+E+N+S)
            		
		#Set the LabelFrame that will contain the form
		labelframe = LabelFrame(self)
		labelframe.grid(padx = 10, pady = 10,row = 1, column= 0, columnspan=2, rowspan=2,sticky = W+E+N+S)
		#Set the number of grid columns and rows inside the LabelFrame, we need 3 rows and 2 column
		for r in range(3):
            		labelframe.rowconfigure(r, weight=1)    
        	for c in range(2):
            		labelframe.columnconfigure(c, weight=1)
            		
		#Set the 1st row 
		self._addressLabel = Label (labelframe, text = "Router IP address:")
		self._addressLabel.grid(column = 0, row = 0, sticky = W+N+S)
		self._ipAddress = StringVar()
		self._ipAddressEntry = Entry(labelframe, textvariable = self._ipAddress)
		self._ipAddressEntry.grid(padx = 5,column = 1, row = 0, sticky = W)
		#Set the 2nd row
		self._snmpLabel = Label (labelframe, text = "SNMP community string:")
		self._snmpLabel.grid(column = 0, row = 1, sticky = W+N+S)
		self._snmpCommunity = StringVar()
		self._snmpCommunity = Entry(labelframe, textvariable = self._snmpCommunity)
		self._snmpCommunity.grid(padx = 5, column = 1, row = 1, sticky = W)
		#Set the 3rd row
		self._startButton = Button(labelframe, text = "Start", command = self._startCmd)
		self._startButton.grid(padx = 5, column = 1, row = 2,sticky = W) 
		
		#create the GUI main loop
		self.mainloop()
	
	def _startCmd(self):
		return

#FOR TESTING		
def main():
	t = TeGUI(None)
	
main()
	
 		
