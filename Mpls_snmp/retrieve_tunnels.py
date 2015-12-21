#from pysnmp.entity.rfc3413.oneliner import cmdgen
from Oid import *
from snmpWrapper import *
from ipaddress import *
"""
def snmpwalk(OID_string):
	cmdGen = cmdgen.CommandGenerator()

	N, R = 0, 25

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

def snmpget(OID_string):
	cmdGen = cmdgen.CommandGenerator()

	errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.getCmd(
	    cmdgen.CommunityData('public', mpModel = 1),
	    cmdgen.UdpTransportTarget(('192.168.3.1', 161)),
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

"""

	

def parse_oid(response_oid):
	#The OID for mpls-te is composed as follows: "resource_oid.tunnel_id.tunnel_instance.source_ip_address.destination_ip_address"
	resource = response_oid[:-4]
	#the ip addresses are in decimal format, so they need convertion
	dest_ip = str(IPv4Address(response_oid[-1]))
	source_ip = str(IPv4Address(response_oid[-2]))
	tun_instance = response_oid[-3]
	tun_id = response_oid[-4]
	return resource, tun_id, tun_instance, source_ip, dest_ip
	
def get_value_from_response(response):
	record = next_record(response)
	if record == -1:
		return
	return record[0][1].prettyPrint()

def main():
	tunnel_name_id = {}
	tunnel_id_info = {}
	tunnel_info_vector = ['mplsTunnelSetupPrio','mplsTunnelHoldingPrio', 'mplsTunnelResourcePointer','mplsTunnelRole','mplsTunnelAdminStatus','mplsTunnelOperStatus']
	cnt = 0
	tunnel_table = []
	num_configured_tun = 0
	num_total_lsp = 0
	resource_tunnel_table = 'mplsTunnelTableEntry'
	resource_num_tunnel = 'mplsTunnelConfigured'
	resource_num_lsp = 'mplsTunnelActive'
	#get the number of configured tunnels
	oid = string_to_OID(resource_num_tunnel)
	response = snmpwalk(oid)

	num_configured_tun = get_value_from_response(response)
	print 'Total number of configured tunnels: ', num_configured_tun
	
	#get the total number of LSP defined at that node	
	oid = string_to_OID(resource_num_lsp)
	response = snmpwalk(oid)

	num_total_lsp = get_value_from_response(response)	
	print 'Total number of LSP: ', num_total_lsp
	
	#get the entire tunnels table
	oid = string_to_OID(resource_tunnel_table)
	response = snmpwalk(oid)
	
	varBindTableRow = next_record(response)
	while varBindTableRow != None:
		name = varBindTableRow[0][0]
		val = varBindTableRow[0][1]
		if val.prettyPrint() == 'No more variables left in this MIB View':
			break
		res, tun_id,tun_instance, source_ip, dest_ip = parse_oid(name)
		"""
		print 'Tunnel ID: ',tun_id,' Tunnel instance: ', tun_instance, ' Source: ', source_ip, ' Dest: ',dest_ip,\
		' Resource: ', OID_to_string(res.prettyPrint()), ' = ', val.prettyPrint()
		"""
		#create a table
		tunnel_table.append([])
		tunnel_table[cnt].append(tun_id)
		tunnel_table[cnt].append(tun_instance)
		tunnel_table[cnt].append(source_ip)
		tunnel_table[cnt].append(dest_ip)
		tunnel_table[cnt].append(OID_to_string(res.prettyPrint()))
		tunnel_table[cnt].append(val.prettyPrint())
		cnt += 1
		varBindTableRow = next_record(response)
	
	for row in tunnel_table:
		if row[4] == 'mplsTunnelDescr' and row[1] != 0:
			tunnel_name_id[row[5]] = []
			tunnel_name_id[row[5]].append(str(row[0]) + '.' + str(row[1]))
			tunnel_name_id[row[5]].append(row[2])
			tunnel_name_id[row[5]].append(row[3])
			tunnel_id_info[str(row[0]) + '.' + str(row[1])] = []
		elif row[4] in tunnel_info_vector and row[1] != 0:
			tunnel_id_info[str(row[0]) + '.' + str(row[1])].append(row[5])
		print row
	print tunnel_name_id
	print tunnel_id_info
		
	for tun_name in tunnel_name_id:
		print 'Tunnel name: ',tun_name
		print '\tTunnel ID:', tunnel_name_id[tun_name][0].split('.')[0]
		print '\tTunnel instance:', tunnel_name_id[tun_name][0].split('.')[1]
		print '\tTunnel source IP address:', tunnel_name_id[tun_name][1]
		print '\tTunnel destination IP address:', tunnel_name_id[tun_name][2]
		i = 0
		for info in tunnel_info_vector:
			print '\t' + info + ': ', tunnel_id_info[tunnel_name_id[tun_name][0]][i]
			i += 1
main()
