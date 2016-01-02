from Tkinter import *

def createFrame(parent, nRows, nCols, labelFrame):
	fr = None
	if labelFrame == 1:
		fr = LabelFrame(parent)
	else:
		fr = Frame(parent)
	for r in range(nRows):
        	fr.rowconfigure(r, weight=1)    
        for c in range(nCols):
            	fr.columnconfigure(c, weight=1)
        return fr
        
def setGridWeight(frame, nRows, nCols):
	for r in range(nRows):
        	frame.rowconfigure(r, weight=1)    
        for c in range(nCols):
            	frame.columnconfigure(c, weight=1)
