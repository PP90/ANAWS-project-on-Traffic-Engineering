from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('public', mpModel=0),
           UdpTransportTarget(('192.168.3.1', 161)),
           ContextData(),
           #ObjectType(ObjectIdentity('SNMPv2-MIB', 'ifInOctets', 1)),
           #ObjectType(ObjectIdentity('SNMPv2-MIB', 'ifOutOctets', 1)))
           ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.10.1")),
           ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.16.1")))
)
	
if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1][0] or '?'
        )
    )
else:
    for varBind in varBinds:
        print(' = '.join([ x.prettyPrint() for x in varBind ]))
