from TeTunnels import *


#R2
#t = TeTunnels("10.1.1.2", "public")
#R1
#t = TeTunnels("192.168.3.1", "public")
#R5
t = TeTunnels("10.5.5.2", "public")

t.start()

confTunnels = t.getConfTunnels()
Lsp = t.getLspTable()

for name in confTunnels.keys():
	print name, str(confTunnels[name])
	
for name in Lsp.keys():
	print name, str(Lsp[name])
