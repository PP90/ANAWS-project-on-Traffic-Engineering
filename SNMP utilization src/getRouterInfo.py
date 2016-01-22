from pysnmp.hlapi import *
import time
import socket, struct
from if_res import if_res
from router import router
from subprocess import call
import subprocess
from pysnmp.entity.rfc3413.oneliner import cmdgen 

debug=0

##Given in input the router address it returns its hostname through SNMP protocol
def get_hostname_SNMP(address, community_name):
	errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),
	CommunityData(community_name, mpModel=0),UdpTransportTarget((address, 161)),
	ContextData(),ObjectType(ObjectIdentity("iso.3.6.1.2.1.1.5.0"))))##Host name
	if errorIndication:
		print(errorIndication)
	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
	hostname=varBinds[0].prettyPrint().split("= ",1)[1];
	return hostname


##Given the address the the interface ID, this function returns the ifInBytes and ifOutBytes from that specific interface.
##In case of error returns -1, -1
def get_in_out_bytes_SNMP(address, if_id, community_name):
	errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),
   	CommunityData(community_name, mpModel=0),
   	UdpTransportTarget((address, 161)),#Address and port
   	ContextData(),ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.10."+`if_id`)),#InOctects
	ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.16."+`if_id`))))#OutOctect
	if errorIndication:
		print(errorIndication)
		return -1,-1
	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
		return -1, -1
	ifInBytes=int(varBinds[0].prettyPrint().split("= ",1)[1]);
	ifOutBytes=int(varBinds[1].prettyPrint().split("= ",1)[1]);
	return ifInBytes,ifOutBytes


##Given the router object in input, this function gets through the SNMP protocol the Router timeUP
def get_timeUp_SNMP(router, community_name):
	errorIndication, errorStatus, errorIndex, varBinds = next(
		    	getCmd(SnmpEngine(),CommunityData(community_name, mpModel=0),
			   	UdpTransportTarget((router.get_address(), 161)),#Address and port
			   	ContextData(),ObjectType(ObjectIdentity("1.3.6.1.2.1.1.3.0"))))#SysUptime

	if errorIndication:
		print(errorIndication)

	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1][0] or '?'))

	timeUp=varBinds[0].prettyPrint().split("= ",1)[1];
	return timeUp

##HERE. TO MODIFY
##Given in input the router address and the number of interfaces of router, the function returns the list of interfaces through SNMP protocol
def get_ifs_info_SNMP(address, number_if, community_name):
	if_list=[];
	i=1;#i is the number of interface
	n=1;#n is used to increment the cycle
	while(n<=number_if):
		errorIndication, errorStatus, errorIndex, varBinds = next(
	    	getCmd(SnmpEngine(),CommunityData(community_name, mpModel=0),
        		   UdpTransportTarget((address, 161)),#Address and port
        		   ContextData(),
			  		ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.5."+`i`)),#IfSpeed (The last number is the interface ID)
			 	 	ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.2."+`i`))#ifTableEntry
					))

		if errorIndication:
			print 'Error indication:'
  			print(errorIndication)
			continue

		elif errorStatus:
			print 'Error Status'
			print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
			continue

		ifSpeed=varBinds[0].prettyPrint().split("= ",1)[1]
		ifName=varBinds[1].prettyPrint().split("= ",1)[1]
		try:
			if_speed_int=int(ifSpeed)
			n=n+1;
			x= if_res(i,ifName, ifSpeed)
			if_list.append(x)
			
		except ValueError:
			if (debug):
				print 'No interface with ID ',i;
		i=i+1;
		
	
	errorIndication, errorStatus, errorIndex, \
	varBindTable = cmdgen.CommandGenerator().bulkCmd(
            cmdgen.CommunityData('public'), cmdgen.UdpTransportTarget((address, 161)),  
            0, 25, ("1.3.6.1.2.1.4.20.1.1"))  # ipAddrTable OID 
	
	i=0
	for varBindTableRow in varBindTable: 
		for var in varBindTableRow:
			ifAddress=var.prettyPrint().split("= ",1)[1]
			print i, ifAddress
			if_list[i].set_address_if(ifAddress)
			i=i+1
	return if_list

##Given in input the router address this function returns the number of interfaces indipendendly either if they are up or down or if they are logical of physical

def get_ifs_number_SNMP(address, community_name):
	errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),
        CommunityData(community_name, mpModel=0),
	UdpTransportTarget((address, 161)),#Address and port
	ContextData(),ObjectType(ObjectIdentity("1.3.6.1.2.1.2.1.0"))#Ifnumber OID
	))

	if errorIndication:
  		print(errorIndication)
	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
			
	if_number=varBinds[0].prettyPrint().split("= ",1)[1];

	if (debug):	
		print '#interfaces: ', if_number;
	return if_number

##Given in input the routers objects list this function prints out the utilization of each interface for each router
def get_utilization_polling(routers_list, how_much_often, community_name):
	n_rel=0;
	in_utilization=0
	out_utilization=0

	while True:
		n_rel=n_rel+1;
		time.sleep(how_much_often);
		for router in routers_list:
			ifs_list=router.get_interfaces();
			print '\n###',n_rel, '(Router ',router.get_hostname(),')'
		
			timeUp=get_timeUp_SNMP(router, community_name)
			timeUp_diff=router.get_timeUp_diff(int(timeUp))

			for interface in ifs_list:
				if_id=int(interface.get_id())
				if_name=interface.get_name()
				if_speed=float(interface.get_if_speed())

				ifInBytes, ifOutBytes = get_in_out_bytes_SNMP(router.get_address(), if_id, community_name)
				delta_ifInBytes=int(ifInBytes)- interface.get_old_in_byte()
				delta_ifOutBytes=int(ifOutBytes)-interface.get_old_out_byte()
				debug=0
				if(debug):
					
					print 'Interface: ',interface.get_name()
					print '[NEW]','IN_Bytes: ', ifInBytes, 'OUT_Bytes: ',ifOutBytes, 'Time_Up: ', timeUp
					print '[OlD]','IN_Bytes: ', interface.get_old_in_byte(), 'OUT_Bytes: ',interface.get_old_out_byte(), 'Time_Up: ', router.get_old_timeUp()
					print 'Delta values: ', delta_ifInBytes, delta_ifOutBytes, timeUp_diff

				interface.set_old_in_byte(ifInBytes)
				interface.set_old_out_byte(ifOutBytes)
				##The utilization takes into account also the 	packets get from SNMP
				if(n_rel>1):
					format(in_utilization,'.3f')
					format(out_utilization,'.3f')
					in_utilization=((delta_ifInBytes)*8*100)/(if_speed*(timeUp_diff/100));
					out_utilization=((delta_ifOutBytes)*8*100)/(if_speed*(timeUp_diff/100));
				
				
				##Some times the shown utilization is bigger than one. This it could be due to buffer o burst packets incoming. In order to avoid this kind of situation, it will be one if it is greater than one. It is correct this line of thinking ?
				
				#if (in_utilization>100): in_utilization=100
				#if (out_utilization>100): out_utilization=100
				

					print '(#', n_rel, ')', ' The  in utilization ', if_name,'interface (ID:', if_id,') is ', in_utilization, '% (if speed: ',if_speed,' )';
					print '(#', n_rel, ')', ' The  out utilization ', if_name,'interface (ID:', if_id,') is ', out_utilization, '% (if speed: ',if_speed,' )\n';
	
##Given in input a router object, this function return the most recent VFile name associated to that router
def open_last_VFile(router):
	hostname=router.get_hostname()
               #Only the files related to that particular roter are considered. Then is taken the most recent
	bash_command='ls VFiles/| egrep "'+hostname+'"|tail -1'
	name_file=subprocess.check_output(bash_command, shell=True)
	name_file=name_file[:-1]#The \n character won't be considered
	return name_file

##Given the namefile, this function returns the timestamp.
##The Vfile format is always the same according to Cisco router MIB specification
def get_timeUp_from_namefile(name_file):
	timeUp=name_file.split("_",1)[1]		
	timeUp=timeUp.split("_",1)[1]
	timeUp=timeUp.split("_",1)[1]
	timeUp=int(timeUp)#The timeUp is encoded in the following way: HHMMSSmmm
	return timeUp

##Given the timestamp extracted from the namefile, if it is less than 100000 (i.e. it is expressed in minutes), then it is converted in seconds and returned
##TODO Actually I suppose that is expressed always in seconds. TO FIX
def convert_in_second(time_up):
	time_up=time_up/100000*60
	return time_up



##given a name file, this function will delete the correspoding (V)file
def delete_file(name_file):
	bash_command='rm -f VFiles/'+name_file
	print subprocess.check_output(bash_command, shell=True)


##Given the object router in input, this function delete all corresponding VFiles
def clear_VFiles(router):
	bash_command='rm -f VFiles/bulktatistics_R'+router.get_hostname()+'*'
	print bash_command
	print subprocess.check_output(bash_command, shell=True)

#Given the name_file (which is the most recent for a specific router) and a router object, this function prints out the in and out utilization of all interfaces of a router. The router object is passed as parameter
def update_info_router(name_file, router):
	in_bytes=-1;
	out_bytes=-1;
        debug=0
	f=open('VFiles/'+name_file, 'r')
	lines= f.readlines()
	if_list=router.get_interfaces()
	ifs_names=[];
	for interface in if_list:
		ifs_names.append(interface.get_name())

	timeUp_diff=router.get_timeUp_diff(get_timeUp_from_namefile(name_file))
	timeUp_diff=int(convert_in_second(timeUp_diff))	
	for idx,name_if in enumerate(ifs_names):
		for line in lines:
			if name_if in line:
				
				tmp=line.split(",",1)[1]	
				tmp=tmp.split(",",1)[1]
				tmp=tmp.split(",",1)[1]
				in_bytes=int(tmp.split(", ",1)[0])
				out_bytes=int(tmp.split(", ",1)[1])
				in_diff, out_diff =router.get_inout_bytes_diff(in_bytes, out_bytes,idx)
                                if_speed=float(router.get_single_interface(idx).get_if_speed())
				
				in_utilization=(in_diff*8*100)/(if_speed*timeUp_diff)
                                out_utilization=(out_diff*8*100)/(if_speed*timeUp_diff)
				router.set_inout_utilization_if(idx, in_utilization, out_utilization)
		
        f.close()
	delete_file(name_file) ##Since that the file is not anymore useful, has to be deleted
	print name_file, ' deleted'
	return router



##Given the addresses list in input, this function returns the routers objects list.
##In particular a router object contains: the router hostname, its time up and a list of interfaces.
#See the router.py src code for more details.

def get_routers_list(addresses_list, community_name):
        routers_list=[]
        for address in addresses_list:
	        ifs_number=int(get_ifs_number_SNMP(address, community_name))
	        r=router(get_hostname_SNMP(address, community_name),address, get_ifs_info_SNMP(address, ifs_number, community_name))
	        routers_list.append(r)
        return routers_list


##Given the object router in input, this function returns two lists: the interfaces names list and the speeds interfaces list
def print_ifs_info(router):
        if_names, if_speeds=router.get_ifs_info() ##Functions asked from Gigi
        for i, interface_name in enumerate(if_names):
                print interface_name, ',',if_speeds[i]
	return if_names, if_speeds



##Get the utilization from a single router through polling
def get_utilization_single_router_polling(single_router, community_name):
	router=single_router[0]
	n_gets=0
	in_utilization=0
	out_utilization=0
	print 'Router: ',router.get_hostname()

	while(n_gets<2):
		ifs_list=router.get_interfaces()
		timeUp=get_timeUp_SNMP(router, community_name)
		timeUp_diff=router.get_timeUp_diff(int(timeUp))
		
		for interface in ifs_list:##For each interface in the router will be get the number of input and output byes
			if_id=int(interface.get_id())
			if_name=interface.get_name()
			if_speed=int(interface.get_if_speed())
			ifInBytes, ifOutBytes = get_in_out_bytes_SNMP(router.get_address(), if_id, community_name)
			delta_ifInBytes=int(ifInBytes)- interface.get_old_in_byte()
			delta_ifOutBytes=int(ifOutBytes)-interface.get_old_out_byte()
			
			debug=0
			if(debug):
				print 'Interface: ',interface.get_name()
				print '[NEW]','IN_Bytes: ', ifInBytes, 'OUT_Bytes: ',ifOutBytes, 'Time_Up: ', timeUp
				print '[OlD]','IN_Bytes: ', interface.get_old_in_byte(), 'OUT_Bytes: ',interface.get_old_out_byte(), 'Time_Up: ', router.get_old_timeUp()
				print 'Delta values: ', delta_ifInBytes, delta_ifOutBytes, timeUp_diff

			interface.set_old_in_byte(ifInBytes)
			interface.set_old_out_byte(ifOutBytes)
		##The utilization takes into account also the packets get from SNMP
			format(in_utilization,'.3f')
			format(out_utilization,'.3f')
			in_utilization=(float(delta_ifInBytes)*8*100)/(if_speed*(timeUp_diff/100));
			out_utilization=(float(delta_ifOutBytes)*8*100)/(if_speed*(timeUp_diff/100));
			interface.set_in_out_utilization(in_utilization, out_utilization)
		n_gets=n_gets+1
		print '#####',n_gets
	router.set_interfaces(ifs_list)
	return router
			


##Given in input the router object, this function returns all interfaces utilization for the router.
##The utilization is computed from data present in the VFiles 
def get_utilization_router_VFile(router_list):
		router=router_list[0]##Actually the router list is composed by one element
		counter=0
		old_name_file=''
		while (counter<2):##Are needed two VFile in order to compute the utilization
			name_file=open_last_VFile(router)
		
			if(old_name_file!=name_file):
				router=update_info_router(name_file, router)
				counter=counter+1
				old_name_file=name_file
			time.sleep(30)
		return router



#######MAIN#############################################

##In some way put the output of buildblablabla file in the addresses list. TODO



##Addresses list in hard coded way
community_name='public'
addresses_list=['192.168.3.1','10.1.1.2']
address=['192.168.3.1']


routers_list=get_routers_list(address, community_name)
routers_list[0].display_info()
#An object router is obtained through this function. 
##What is needed are two parameter: the address of the router and the community name
r=get_routers_list(address, community_name)##Return a router list giving in input the addresses list
my_router=router()##Router without information. Used later

##Example #1 (Utilizations through VFile)
##The utilizations of interfaces of a single router r are obtained.
##The utilizations are obtained waiting 2 VFile sent by router r itself.
#Only the router object needed for this function.
#It takes at least one minute to see the output results.
utilization_VFile_once=0
if(utilization_VFile_once):
	my_router=get_utilization_router_VFile(r)##Return the router with the utilization by VFiles
	my_router.print_ifs_utilization()##print the interfaces utilizations of the router

##Example #2(Utilizations through NOT periodic polling)
##The utilizations of interfaces of a single router r are obtained.
##The utilizations are obtained polling twice the information from the router.
##Is necessary polling twice because to compute the utilizations.
##Needed to parameters : the router object (r) and the community name.
polling=0
if(polling):
	my_router=get_utilization_single_router_polling(r, community_name)##Polling a specific router
	my_router.print_ifs_utilization()##print the interfaces utilizations of the router

##Example #3(Utilizations through periodic polling)
##The utilizations of interfaces of all routers are obtained.
##The utilizations are obtained polling periodically all the information from all routers in the routers list.
##These parameters are needed: the routers_list, polling_interval and commnunity name.
##The routers_list can be obtained using the get_routers_list function.
polling_periodic=1
if(polling_periodic):
	polling_interval=1##SECONDS
	get_utilization_polling(routers_list, polling_interval, community_name)
	
##print_ifs_info(routers_list[0]) //Function asked for Luigi

