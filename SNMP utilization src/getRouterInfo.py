from pysnmp.hlapi import *
import time
import socket, struct
from if_res import if_res
from router import router
from subprocess import call
import subprocess

debug=0

##Given in input the router address it returns its hostname through SNMP protocol
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



##Given in input the router address and the number of interfaces of router, the function returns the list of interfaces
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



##Given in input the router address this function returns the number of interfaces indipendendly if they are up or down
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

##Given in input an address router this function prints out the utilization at each interface
##TODO: generalize for n addresses
def get_utilization_polling(address):
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
	
##Given in input a router Object, this function return the most recent VFile associated to that router
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

##Given the timestamp extracted from the namefile, if it is less than 100000 (i.e. it is expressed in minutes), then it is converted in seconds and returned.
def convert_in_second(time_up):
	time_up=time_up/100000*60
	return time_up

#Given the name_file (which is the most recent for a specific router) and a router object, this function prints out the in and out utilization of all interfaces of a router passed as parameter as an Object
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
	print "timeUp diff in seconds: ",timeUp_diff
	for idx,name_if in enumerate(ifs_names):
		for line in lines:
			if name_if in line:
				
				tmp=line.split(",",1)[1]	
				tmp=tmp.split(",",1)[1]
				tmp=tmp.split(",",1)[1]
				in_bytes=int(tmp.split(", ",1)[0])
				out_bytes=int(tmp.split(", ",1)[1])
				in_diff, out_diff =router.get_inout_bytes_diff(in_bytes, out_bytes,idx)
                                if_speed=float(router.get_interface(idx).get_if_speed())
				in_utilization=(in_diff*8*100)/(if_speed*timeUp_diff);
                                out_utilization=(out_diff*8*100)/(if_speed*timeUp_diff);
				print '(IN)Utiliz. : ',in_utilization,'%'
                                print '(OUT)Utiliz. : ',out_utilization,'%'					
        ##Since that the file is not anymore useful, has to be deleted.TODO	
        f.close()


##Given the addresses list in input, this function returns the routers list object.
##In particular a router object contains: the router hostname, its time up and a list of interfaces
def get_routers_list(addresses_list):
        routers_list=[]
        for address in addresses_list:
	        ifs_number=int(get_if_number(address))
	        r=router(get_hostname(address),address, get_ifs_info(address, ifs_number))
	        routers_list.append(r)
        return routers_list


##Given ininput the routers list, this function return all interfaces utilization for each router. The utilization is computed from data present in the VFiles 
def get_utilization_from_VFile(routers_list):
        while True:
                for router in routers_list:
                        print 'To implement\n'
                        ##TODO Generalize the code to obtain the interfaces utilization for all router in the router list


def get_ifs_info(router):
        if_names, if_speeds=router.get_ifs_info() ##Functions asked from Gigi
        for i, interface_name in enumerate(if_names):
                print interface_name, ',',if_speeds[i]
	return if_names, if_speeds


#######MAIN
##In some way put the output of buildblablabla file in the addresses list. TODO
polling=0
addresses_list=['192.168.3.1','10.1.1.2']##Addresses list in hard coded way
routers_list=get_routers_list(addresses_list)
##get_ifs_info(routers_list[0]) //Function asked for Luigi


counter=0
old_name_file='';

while True:
	counter=counter+1
	print "\n\n###",counter
        if(counter==1):
                print "!!!!!!!The first time the utilization has not be taken in consideration!"

	name_file=open_last_VFile(routers_list[1])

	if(old_name_file==name_file):##This happens when it doesn't received a new VFile
		print 'Something is not changed. Nothing will be updated'
	else:
		print 'Something is changed in router ',routers_list[1].get_hostname() +'. Information will be updated.'
		update_info_router(name_file, routers_list[1])
		#for router in routers_info:
		#	router.display_info()
		#	print '\n'

	old_name_file=name_file
	time.sleep(30)

if(polling):
	get_utilization(address, r)
	
