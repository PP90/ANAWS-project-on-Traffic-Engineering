from Tkinter import *
import tkFont
from PIL import Image

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
		root = Tk()
		Frame.__init__(self,root)
		#Set the window title
		self.master.title("TE Dashboard")
		#Set the window size
		self.master.geometry("600x400")
		self.grid()
		#Set the number of grid columns and rows, for the moment we need 4 rows and 2 column
		for r in range(2):
            		self.master.rowconfigure(r, weight=1)    
        	for c in range(1):
            		self.master.columnconfigure(c, weight=1)
		
		#Set the first label string
		self._titleFont = tkFont.Font(family = "Verdana", size = 16, weight = "bold")
		self._title = Label (self, font = self._titleFont, justify = CENTER, text = "Traffic Engineering Dashboard")
		self._title.grid(column = 0, row = 0,  columnspan = 2, sticky = W+E+N+S)
		#Set the 1st row 
		self._addressLabel = Label (self, text = "Router IP address:")
		self._addressLabel.grid(column = 0, row = 1, sticky = W+N+S)
		self._ipAddress = StringVar()
		self._ipAddressEntry = Entry(self, textvariable = self._ipAddress)
		self._ipAddressEntry.grid(column = 1, row = 1, sticky = W+E+N+S)
		#Set the 2nd row
		self._snmpLabel = Label (self, text = "SNMP community string:")
		self._snmpLabel.grid(column = 0, row = 2, sticky = W+N+S)
		self._snmpCommunity = StringVar()
		self._snmpCommunity = Entry(self, textvariable = self._snmpCommunity)
		self._snmpCommunity.grid(column = 1, row = 2, sticky = W+E+N+S)
		#Set the 3rd row
		self._startButton = Button(self, text = "Start", command = self._startCmd)
		self._startButton.grid(column = 1, row = 3,sticky = W+E+N+S) 
		
		#create the GUI main loop
		self.mainloop()
	
	def _startCmd(self):
		return

#FOR TESTING		
def main():
	t = TeGUI(None)
	
main()
	
 		
