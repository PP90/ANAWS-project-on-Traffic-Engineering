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
