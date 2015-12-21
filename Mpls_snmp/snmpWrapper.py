from pysnmp.hlapi import *

def snmpwalk(oid):
	bulk = bulkCmd(
		SnmpEngine(),
                CommunityData('public'),
                UdpTransportTarget(('192.168.3.1', 161)),
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
		
		
def snmpget(oid):
	errorIndication, errorStatus, errorIndex, varBinds = next(
    		getCmd(SnmpEngine(),
		   CommunityData('public'),
		   UdpTransportTarget(('192.168.3.1', 161)),
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
