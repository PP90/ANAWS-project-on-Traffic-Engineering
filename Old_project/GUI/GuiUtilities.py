from Tkinter import *
import ttk
from SNMP_utilization_src.if_res import *
from SNMP_utilization_src.router import *

def createFrame(parent, nRows, nCols, labelFrame = False, msg = None):
	fr = None
	if labelFrame == True:
		fr = LabelFrame(parent, text=msg)
	else:
		fr = Frame(parent)
	for r in range(nRows):
        	fr.rowconfigure(r, weight=1)    
        for c in range(nCols):
            	fr.columnconfigure(c, weight=1)
        return fr
        
def setGridWeight(frame, nRows, nCols, WeightsRows = None, WeightsCols = None):
	for r in range(nRows):
		if WeightsRows == None:
        		frame.rowconfigure(r, weight=1)  
        	else:
        		frame.rowconfigure(r, weight=WeightsRows[r])  
        for c in range(nCols):
            	if WeightsCols == None:
        		frame.columnconfigure(c, weight=1)  
        	else:
        		frame.columnconfigure(c, weight=WeightsCols[c])  

def centerWindow(frame, w = 600, h = 400):
	try:
		sw = frame.master.winfo_screenwidth()
		sh = frame.master.winfo_screenheight()
	except:
		sw = frame.winfo_screenwidth()
		sh = frame.winfo_screenheight()
	x = (sw - w)/2
	y = (sh - h)/2
	try:
		frame.master.geometry('%dx%d+%d+%d' % (w,h,x,y))
	except:
		frame.geometry('%dx%d+%d+%d' % (w,h,x,y))
		
def createTreeView(frame, columnsName, routerObjList = None):
	tree = ttk.Treeview(frame)
	columnsID = []
	for colId in range(len(columnsName)-1):
		columnsID.append(str(colId + 1))
	columnsID = tuple(columnsID)
	tree["columns"] = columnsID
	tree.heading('#0', text = columnsName[0])
	for colId in columnsID:
		tree.column(colId, width=100)
		tree.heading(colId, text = columnsName[int(colId)])
	
	if routerObjList != None:
		addRoutersToTree(tree,routerObjList)
	
	return tree

#It expects that there are at least 3 columns: "Router name", "IP address" and "Connected to"
def addRoutersToTree(tree, routerObjList):
	for router in routerObjList:
		name = router.get_hostname()
		address = router.get_address()
		print "ROUTER: ", name
		interfacesList = router.get_interfaces()
		#Add the router node as a parent node
		tree.insert("", 'end', name, text = name, values = (address,""))	
		for interface in interfacesList:
			IfName = interface.get_name()
			IfAddress = interface.get_address_if()	
			ID = interface.get_id()	
			IfSubnetMask = interface.get_subnet_if()
			print "\tInterface: ", IfName, "ID: " ,ID,"IP addr: ", IfAddress
			#Add the interface node as a child node of its router node
			tree.insert(name, 'end', name+IfName, text = IfName, values = (IfAddress, IfSubnetMask,""))
			
