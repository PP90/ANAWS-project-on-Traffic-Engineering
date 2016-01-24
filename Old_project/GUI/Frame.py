from Tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.geometry("600x400")
        self.master.title("Grid Manager")
        self.grid()

        for r in range(6):
            self.master.rowconfigure(r, weight=1)    
        for c in range(5):
            self.master.columnconfigure(c, weight=1)
            Button(master, text="Button {0}".format(c)).grid(row=6,column=c,sticky=E+W)

        Frame1 = Frame(master, bg="red")
        Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S) 
        Frame2 = Frame(master, bg="blue")
        Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = W+E+N+S)
        Frame3 = Frame(master, bg="green")
        Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = W+E+N+S)

root = Tk()
app = Application(master=root)
app.mainloop()
