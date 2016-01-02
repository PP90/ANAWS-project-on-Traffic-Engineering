from Tkinter import *

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
