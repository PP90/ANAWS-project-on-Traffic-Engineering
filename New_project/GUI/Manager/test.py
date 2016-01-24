import manager as man
import pprint

m1 = man.Manager("192.168.3.1", "public")

a = m1.getTopology()
print("\n\n matrix")
pprint.pprint(a)

#a = m1.getListIP()
#print("\n\n list")
#pprint.pprint(a)

#a = m1.listInfo
#print("\n\n listInfo")
#pprint.pprint(a)

#a = m1.getUtilization("1.1.1.1")
#print("\n\n result")
#pprint.pprint(a)
#a = m1.listInfo
#print("\n\n listInfo")
#pprint.pprint(a)

t = m1.getTunnel("1.1.1.1")
print("\n Tunnels")
print(t)
