from Tkinter import *

root = Tk()

labelframe = LabelFrame(root)
labelframe.pack(fill="both", expand="yes")
 
left = Label(labelframe, text="Inside the LabelFrame")
left.pack()
 
root.mainloop()
