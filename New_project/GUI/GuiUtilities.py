from Tkinter import *
import ttk
from Manager.SNMP_utilization_src.if_res import *
from Manager.SNMP_utilization_src.router import *


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
		
def createTreeView(frame, columnsName, routerObjList = None, topologyMatrix = None, allInterfaces = 1):
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
	
	if routerObjList != None and topologyMatrix != None:
		addRoutersToTree(tree,routerObjList, topologyMatrix, allInterfaces)
	
	elif routerObjList != None:
		addRoutersToTree(tree,routerObjList, allInterfaces)
	
	return tree

#It expects that there are at least 3 columns: "Router name", "IP address" and "Connected to"
def addRoutersToTree(tree, routerObjList, topologyMatrix = None, allInterfaces = 1):
	i = 0
	for router in routerObjList:
		nextHopRouterList = []
		name = router.get_hostname()
		address = router.get_address()
		#print "ROUTER: ", name
		interfacesList = router.get_interfaces()
		if topologyMatrix != None:
			#Pick the row in the topology matrix relative to the given router
			topologyRow = topologyMatrix[i]
		#Add the router node as a parent node
		tree.insert("", 'end', name, text = name, values = (address,""))	
		for interface in interfacesList:
			nextHopRouter = ''
			IfName = interface.get_name()
			IfAddress = interface.get_address_if()
			if IfAddress == None and allInterfaces == 0:
				continue	
			ID = interface.get_id()	
			IfSubnetMask = interface.get_subnet_if()
			#print "\tInterface: ", IfName, "ID: " ,ID,"IP addr: ", IfAddress
			if topologyMatrix != None:
				#Look to which other router this interface is attached
				if IfAddress in topologyRow:
					#The position of this address inside the row gives next-hop router: column X-1 => router X 
					pos = topologyRow.index(IfAddress)
					print topologyRow, pos, IfAddress
					#With the position you can retrieve the router names
					nextHopRouter = routerObjList[pos].get_hostname()
					nextHopRouterList.append(nextHopRouter)
				
			#Add the interface node as a child node of its router node
			tree.insert(name, 'end', name+IfName, text = IfName, values = (IfAddress, IfSubnetMask,nextHopRouter))
		#For this router set the list of other attached routers
		tree.set(name, tree["columns"][-1], ', '.join(nextHopRouterList))
		i += 1
