from pysnmp.entity.rfc3413.oneliner import cmdgen
from Oid import *
#from pysnmp.hlapi import *
from ipaddress import *

def snmpwalk(OID_string):
	cmdGen = cmdgen.CommandGenerator()

	N, R = 1, 25

	errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
	    cmdgen.CommunityData('public', mpModel = 1),
	    cmdgen.UdpTransportTarget(('192.168.3.1', 161)),
	    N, R,
	    OID_string,
	    lookupNames=False, lookupValues=False
	)

	if errorIndication:
	    print(errorIndication)
	    return -1
	else:
	    if errorStatus:
		print('%s at %s' % (
		    errorStatus.prettyPrint(),
		    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
		    )
		)
		return -1
	    else:
	    	return varBindTable
		#for varBindTableRow in varBindTable:
		    #for name, val in varBindTableRow:
		        #print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

def parse_oid(response_oid):
	#The OID for mpls-te is composed as follows: "resource_oid.tunnel_id.tunnel_instance.source_ip_address.destination_ip_address"
	resource = response_oid[:-4]
	#the ip addresses are in decimal format, so they need convertion
	dest_ip = str(IPv4Address(response_oid[-1]))
	source_ip = str(IPv4Address(response_oid[-2]))
	tun_instance = response_oid[-3]
	tun_id = response_oid[-4]
	return resource, tun_id, tun_instance, source_ip, dest_ip
	
	

def main():
	resource = 'mplsTunnelTableEntry'
	oid = string_to_OID(resource)
	response = snmpwalk(oid)
	if response < 0:
		return
	
	cnt = 0
	tunnel_table = []
	for varBindTableRow in response:
		    for name, val in varBindTableRow:
		        res, tun_id,tun_instance, source_ip, dest_ip = parse_oid(name)
		        print 'Tunnel ID: ',tun_id,' Tunnel instance: ', tun_instance, ' Source: ', source_ip, ' Dest: ',dest_ip,\
		        ' Resource: ', OID_to_string(res.prettyPrint()), ' = ', val.prettyPrint()
		        #create a table
		        tunnel_table.append([])
		        tunnel_table[cnt].append(tun_id)
		        tunnel_table[cnt].append(tun_instance)
		        tunnel_table[cnt].append(source_ip)
		        tunnel_table[cnt].append(dest_ip)
		        tunnel_table[cnt].append(OID_to_string(res.prettyPrint()))
		        tunnel_table[cnt].append(val.prettyPrint())
			cnt += 1
	
	for row in tunnel_table:
		print row

main()
