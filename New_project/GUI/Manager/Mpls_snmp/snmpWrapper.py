from pysnmp.hlapi import *

def snmpwalk(oid, address, community):
	bulk = bulkCmd(
		SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((address, 161)),
                ContextData(),
                1, 25,
                ObjectType(ObjectIdentity(oid)),
                lookupMib = False,
                lexicographicMode=False)
        
	return bulk
	
def next_record(cmd_instance):
	errorIndication, errorStatus, errorIndex, varBinds = next(cmd_instance)

	if errorIndication:
		print(errorIndication)
		return -1
	elif errorStatus:
		print('%s at %s' % (
		        errorStatus.prettyPrint(),
		        errorIndex and varBinds[int(errorIndex)-1][0] or '?'
		    )
		)
		return -1
	else:
		return varBinds
		
		
def snmpget(oid, address, community):
	errorIndication, errorStatus, errorIndex, varBinds = next(
    		getCmd(SnmpEngine(),
		   CommunityData(community),
		   UdpTransportTarget((address, 161)),
		   ContextData(),
		   ObjectType(ObjectIdentity(oid)))
	)

	if errorIndication:
		print(errorIndication)
		return -1
	elif errorStatus:
		print('%s at %s' % (
		        errorStatus.prettyPrint(),
		        errorIndex and varBinds[int(errorIndex)-1][0] or '?'
		    )
		)
		return -1
	else:
		return varBinds
