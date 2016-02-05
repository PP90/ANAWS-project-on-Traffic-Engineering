from Tkinter import *
import ttk
root = Tk()

tree = ttk.Treeview(root)
tree["columns"]=("1","2")
tree.column("1", width=100 )
tree.column("2", width=100)

tree.heading('#0', text='Router name')
tree.heading("1", text="Ip address")
tree.heading("2", text="Connected to")

#R1
tree.insert("", 'end', "R1", text="R1", values=("1.1.1.1",""))
tree.insert("R1", 'end', text="Fe0/0", values=("192.168.3.1", "localhost"))
tree.insert("R1", 'end', text="Fe0/1", values=("10.1.1.1", "R2"))
tree.insert("R1", 'end', text="Fe0/2", values=("10.3.3.1", "R3"))
#R2
tree.insert("", 'end', "R2", text="R2", values=("2.2.2.2",""))
tree.insert("R2", 'end', text="Fe0/1", values=("10.1.1.2", "R1"))
tree.insert("R2", 'end', text="Fe0/2", values=("10.5.5.1", "R5"))


tree.pack()
root.mainloop()
