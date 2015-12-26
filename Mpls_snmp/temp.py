#from pysnmp.entity.rfc3413.oneliner import cmdgen
from Oid import *
from snmpWrapper import *
from ipaddress import *
	

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
	result = record[0][1].prettyPrint()
	if result == 'No more variables left in this MIB View':
		return None
	else:
		return result

def create_OID_matrix(response):
	OID_matrix = []
	cnt = 0
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
		OID_matrix.append([])
		OID_matrix[cnt].append(tun_id)
		OID_matrix[cnt].append(tun_instance)
		OID_matrix[cnt].append(source_ip)
		OID_matrix[cnt].append(dest_ip)
		OID_matrix[cnt].append(OID_to_string(res.prettyPrint()))

		OID_matrix[cnt].append(val.prettyPrint())
		cnt += 1
		varBindTableRow = next_record(response)
	return OID_matrix

def populate_tunnel_configs_table(row, config_vect, tunnel_configs):
	#if the Instance field is equal to 0 it means that this is a row regarding the tunnel configuration
	if row[1] != 0:
		return
	if row[4] in config_vect:
		index = config_vect.index(row[4])
		#for the moment the only solution to distinguish the tunnel configurations from each other is to use as index: "ID.Instance.SourceIP.DestIP"
		if str(row[0]) + '.' + str(row[1]) + '.' + str(row[2]) + '.' + str(row[3]) not in tunnel_configs.keys():
			tunnel_configs[str(row[0]) + '.' + str(row[1]) + '.' + str(row[2]) + '.' + str(row[3])] = []
		tunnel_configs[str(row[0]) + '.' + str(row[1]) + '.' + str(row[2]) + '.' + str(row[3])].insert(index,row[5])
		
#TODO: now it gets only ipv4 addresses: I've to implement also the ipv6 part
def get_configured_path(prim_index, second_index):
	hops = []
	singleHop = ''
	addrPrefix = 0
	oid = string_to_OID('mplsTunnelHopAddrType')
	oid = oid + '.' + prim_index + '.' +  second_index
	responseAddrType = snmpwalk(oid)
	oid = ''
	addrType =  get_value_from_response(responseAddrType)
	#IPv4 address
	if addrType == '1':
		oid = string_to_OID('mplsTunnelHopIpv4Addr')
	#IPv6 address
	elif addrType == '2':
		oid = string_to_OID('mplsTunnelHopIpv6Addr')

	oid = oid + '.' + prim_index + '.' +  second_index
	responseHop = snmpwalk(oid)
	oid = ''
	#IPv4 address
	if addrType == '1':
		oid = string_to_OID('mplsTunnelHopIpv4PrefixLen')
	#IPv6 address
	elif addrType == '2':
		oid = string_to_OID('mplsTunnelHopIpv6PrefixLen')
	oid = oid + '.' + prim_index + '.' +  second_index
	responsePrefix = snmpwalk(oid)
	while addrType != None:
		singleHop =  get_value_from_response(responseHop)
		addrPrefix =  get_value_from_response(responsePrefix)
		if singleHop == None or addrPrefix == None:
			continue
		hops.append(str(IPv4Address(int(singleHop,0))) + '/' + str(addrPrefix))
		addrType =  get_value_from_response(responseAddrType)
	return hops
		
	
def retrieve_conf(tun_name,tunnel_configs, config_vect):
	table = tunnel_configs.values()
	for vect in table:
		if vect[config_vect.index('mplsTunnelDescr')] == tun_name:
			return vect

def main():
	tunnel_name_id = {}
	tunnel_id_info = {}
	tunnel_configs = {}
	tunnel_info_vector = ['mplsTunnelSetupPrio','mplsTunnelHoldingPrio', 'mplsTunnelResourcePointer','mplsTunnelRole','mplsTunnelAdminStatus','mplsTunnelOperStatus']
	config_vect = ['mplsTunnelName','mplsTunnelDescr','mplsTunnelHopTableIndex', 'mplsTunnelPathInUse']
	OID_matrix = []
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
	
	#create the OID matrix in order to filter and retrieve the needed data
	OID_matrix = create_OID_matrix(response)
	
	for row in OID_matrix:
		populate_tunnel_configs_table(row, config_vect, tunnel_configs)
		if row[4] == 'mplsTunnelDescr' and row[1] != 0:
			tunnel_name_id[row[5]] = []
			tunnel_name_id[row[5]].append(str(row[0]) + '.' + str(row[1]))
			tunnel_name_id[row[5]].append(row[2])
			tunnel_name_id[row[5]].append(row[3])
			tunnel_id_info[str(row[0]) + '.' + str(row[1])] = []
		elif row[4] in tunnel_info_vector and row[1] != 0:
			index = tunnel_info_vector.index(row[4])
			tunnel_id_info[str(row[0]) + '.' + str(row[1])].insert(index,row[5])
			
	#-----------FOR TESTING-----------#		
		#print row
	#print tunnel_name_id
	#print tunnel_id_info
	print tunnel_configs
		
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
		configuration = retrieve_conf(tun_name,tunnel_configs,config_vect)
		if configuration != None:
			i = 0
			for info in config_vect:
				print '\t' + info + ': ', configuration[i]
				i += 1
			path = get_configured_path(configuration[config_vect.index('mplsTunnelHopTableIndex')], configuration[config_vect.index('mplsTunnelPathInUse')])
			print '\tTunnel path:', path
main()
