##TO DO
##The address, the port, the community name have to be passed as parameters in the function and not set manually as now

from pysnmp.hlapi import *
import time
import socket, struct
from if_res import if_res

##Actually doesn't give the gateway address. To fix
def get_default_gateway_linux():
	with open("/proc/net/route") as fh:
		for line in fh:
			fields = line.strip().split()
			if fields[1] != '00000000' or not int (fields[3], 16) & 2:
				continue

	return socket.inet_ntoa(struct.pack("<L", int(fields[2],16)))


##This fuction returns for each interface its speed expressed in bit per second
def get_ifs_info(number_if):
	id_ifs=[];
	if_list=[];
	i=1;#i is the number of interface
	n=1;#n is used to increment the cycle
	while(n<=number_if):
		errorIndication, errorStatus, errorIndex, varBinds = next(
	    	getCmd(SnmpEngine(),
        		   CommunityData('public', mpModel=0),
        		   UdpTransportTarget(('192.168.3.1', 161)),#Address and port
        		   ContextData(),
			  		ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.5."+`i`)),#IfSpeed (The last number is the interface ID)
			 	 	ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.2."+`i`))#ifTableEntry
					)
		)

		if errorIndication:
			print 'Error indication:'
  			print(errorIndication)
			continue;

		elif errorStatus:
			print 'Error Status'
			print('%s at %s' % (
				errorStatus.prettyPrint(),
			errorIndex and varBinds[int(errorIndex)-1][0] or '?'
        		))
			continue;

		ifSpeed=varBinds[0].prettyPrint().split("= ",1)[1];
		ifName=varBinds[1].prettyPrint().split("= ",1)[1];
		try:
			if_speed_int=int(ifSpeed)
			n=n+1;
			x= if_res(i,ifName, ifSpeed)
			id_ifs.append(x)
			
		except ValueError:
			print 'No interface with ID = ',i;
		i=i+1;
	return id_ifs



##This function returns the number of interfaces indipendendly if thet are up or down
def get_if_number():
	errorIndication, errorStatus, errorIndex, varBinds = next(
	    getCmd(SnmpEngine(),
        	   CommunityData('public', mpModel=0),
        	   UdpTransportTarget(('192.168.3.1', 161)),#Address and port
        	   ContextData(),
		  		ObjectType(ObjectIdentity("1.3.6.1.2.1.2.1.0"))#Ifnumber OID
		 	 )
	)

	if errorIndication:
  		print(errorIndication)
	elif errorStatus:
		print('%s at %s' % (
			errorStatus.prettyPrint(),
			errorIndex and varBinds[int(errorIndex)-1][0] or '?'
        	)
    	)
			
	if_number=varBinds[0].prettyPrint().split("= ",1)[1];
	print '#interfaces: ', if_number;
	return if_number

##Given a if_resource instance this functions gets its utilization
def get_utilization(if_list):
	
	old_ifInBytes=0;
	old_ifOutBytes=0;
	old_TimeUp=0;
	how_much_often=1;

	while True:
		time.sleep(how_much_often);
		print '\n\n'
		for x in ifs_list:
			if_id=int(x.get_id())
			if_name=x.get_name()
			if_speed=float(x.get_if_speed())
		
			
		
			errorIndication, errorStatus, errorIndex, varBinds = next(
		    	getCmd(SnmpEngine(),
			   	CommunityData('public', mpModel=0),
			   	UdpTransportTarget(('192.168.3.1', 161)),#Address and port
			   	ContextData(),
		   			ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.10."+`if_id`)),#InOctects
		   			ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.16."+`if_id`)),#OutOctect
			 		ObjectType(ObjectIdentity("1.3.6.1.2.1.1.3.0"))#SysUptime
			 	 	))

			if errorIndication:
	  			print(errorIndication)
			elif errorStatus:
				print('%s at %s' % (
					errorStatus.prettyPrint(),
					errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
			
	
	
			ifInBytes=int(varBinds[0].prettyPrint().split("= ",1)[1]);
			ifOutBytes=int(varBinds[1].prettyPrint().split("= ",1)[1]);
			#timeUp=int(varBinds[2].prettyPrint().split("= ",1)[1]);

			delta_ifInBytes=float(ifInBytes)- x.get_old_in_byte()
			delta_ifOutBytes=float(ifOutBytes)-x.get_old_out_byte()
	
			x.set_old_in_byte(ifInBytes)
			x.set_old_out_byte(ifOutBytes)
			
			#print 'In and out bytes ', ifInBytes, ifOutBytes
			#print 'In and out bytes (OLD)', old_ifInBytes, old_ifOutBytes
			#print 'delta values: ', delta_ifInBytes, delta_ifOutBytes
	
			old_ifInBytes=ifInBytes;
			old_ifOutBytes=ifOutBytes;
	
			#old_TimeUp=timeUp;
	
			utilization=(delta_ifInBytes+delta_ifOutBytes)*8*100/(if_speed*how_much_often);##The utilization takes into account also the 	packets get from SNMP
			print 'The utilization ',if_name,' interface (ID:', if_id,') is ', utilization, '% (if speed: ',if_speed,' )';

#######MAIN
##First to get the if_number is needed to get the next hop address is some way. I'm assuming that the next hop address is 192.168.3.1
ifs_number=int(get_if_number())
ifs_list=get_ifs_info(ifs_number);
how_much_often=1
get_utilization(ifs_list)
##Print all interfaces info
'''
for x in ifs_list:
	print x.display_info()
'''
	
	
