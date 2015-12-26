from TeTunnels import *


t = TeTunnels("10.1.1.2", "public")

t.start()

confTunnels = t.getConfTunnels()
Lsp = t.getLspTable()

for name in confTunnels.keys():
	print name, str(confTunnels[name])
	
for name in Lsp.keys():
	print name, str(Lsp[name])
