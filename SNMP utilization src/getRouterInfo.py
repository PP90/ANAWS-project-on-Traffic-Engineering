from pysnmp.hlapi import *
import time
import socket, struct
from if_res import if_res
from router import router

debug=0

##Function to get Host name
def get_hostname(address):
	errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),
	CommunityData('public', mpModel=0),UdpTransportTarget((address, 161)),
	ContextData(),ObjectType(ObjectIdentity("iso.3.6.1.2.1.1.5.0"))))##Host name
	if errorIndication:
		print(errorIndication)
	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
	hostname=varBinds[0].prettyPrint().split("= ",1)[1];
	return hostname



##This fuction returns for each interface its speed expressed in bit per second
def get_ifs_info(address, number_if):
	id_ifs=[];
	if_list=[];
	i=1;#i is the number of interface
	n=1;#n is used to increment the cycle
	while(n<=number_if):
		errorIndication, errorStatus, errorIndex, varBinds = next(
	    	getCmd(SnmpEngine(),
        		   CommunityData('public', mpModel=0),
        		   UdpTransportTarget((address, 161)),#Address and port
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
			if (debug):
				print 'No interface with ID ',i;
		i=i+1;
	return id_ifs



##This function returns the number of interfaces indipendendly if they are up or down
def get_if_number(address):
	errorIndication, errorStatus, errorIndex, varBinds = next(
	    getCmd(SnmpEngine(),
        	   CommunityData('public', mpModel=0),
        	   UdpTransportTarget((address, 161)),#Address and port
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
	if (debug):	
		print '#interfaces: ', if_number;
	return if_number

##Given a if_resource instance this functions gets its in and out utilization
def get_utilization(address, r):
	old_ifInBytes=0;
	old_ifOutBytes=0;
	old_TimeUp=0;
	how_much_often=1;
	n_rel=0;
	while True:
		n_rel=n_rel+1;
		time.sleep(how_much_often);
		print '\n'
		for x in ifs_list:
			if_id=int(x.get_id())
			if_name=x.get_name()
			if_speed=float(x.get_if_speed())
		
			
		
			errorIndication, errorStatus, errorIndex, varBinds = next(
		    	getCmd(SnmpEngine(),
			   	CommunityData('public', mpModel=0),
			   	UdpTransportTarget((address, 161)),#Address and port
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
			if(n_rel>1):
				ifInBytes=int(varBinds[0].prettyPrint().split("= ",1)[1]);
				ifOutBytes=int(varBinds[1].prettyPrint().split("= ",1)[1]);
				timeUp=int(varBinds[2].prettyPrint().split("= ",1)[1]);

				delta_ifInBytes=int(ifInBytes)- x.get_old_in_byte()
				delta_ifOutBytes=int(ifOutBytes)-x.get_old_out_byte()
				delta_timeUp=int(timeUp)-x.get_old_timeUp()

				if(debug):
					print 'IN OUT bytes and TIME (NEW)', ifInBytes, ifOutBytes, timeUp
					print 'IN OUT bytes and TIME (OLD)', x.get_old_in_byte(), x.get_old_out_byte(), x.get_old_timeUp()
					print 'delta values: ', delta_ifInBytes, delta_ifOutBytes, delta_timeUp
		
				x.set_old_in_byte(ifInBytes)
				x.set_old_out_byte(ifOutBytes)
				x.set_old_timeUp(timeUp)
				
				##The utilization takes into account also the 	packets get from SNMP
				in_utilization=((delta_ifInBytes)*8*100)/(if_speed*(delta_timeUp/100));
				out_utilization=((delta_ifOutBytes)*8*100)/(if_speed*(delta_timeUp/100));
				format(in_utilization,'.3f')
				format(out_utilization,'.3f')
				
				##Some times the shown utilization is bigger than one. This it could be due to buffer o burst packets incoming. In order to avoid this kind of situation, it will be one if it is greater than one. It is correct this line of thinking ?
				
				#if (in_utilization>100): in_utilization=100
				#if (out_utilization>100): out_utilization=100
				

				print '(#', n_rel, ')', ' The  in utilization ', if_name,'interface (ID:', if_id,') is ', in_utilization, '% (if speed: ',if_speed,' )';
				print '(#', n_rel, ')', ' The  out utilization ', if_name,'interface (ID:', if_id,') is ', out_utilization, '% (if speed: ',if_speed,' )\n';
	
			

#######MAIN
##In some way put the output of buildblablabla file in this list. TODO
addresses=['10.1.1.2','192.168.3.1']
routers_info=[]
for address in addresses:
	ifs_number=int(get_if_number(address))
	r=router(get_hostname(address),address, get_ifs_info(address, ifs_number))
	routers_info.append(r)
	r.display_info()

#get_utilization(address, r) In case of polling utilizzation

	
