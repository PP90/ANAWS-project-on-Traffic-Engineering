from pysnmp.hlapi import *
import time

##In caso di errore ritornare -1
def get_if_speed():
	errorIndication, errorStatus, errorIndex, varBinds = next(
	    getCmd(SnmpEngine(),
        	   CommunityData('public', mpModel=0),
        	   UdpTransportTarget(('192.168.3.1', 161)),#Address and port
        	   ContextData(),
		  		ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.5.1"))#IfSpeed
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
			
	ifSpeed=varBinds[0].prettyPrint().split("= ",1)[1];
	return ifSpeed


if_speed=float(get_if_speed());
old_ifInBytes=0;
old_ifOutBytes=0;
old_TimeUp=0;
how_much_often=1;
while True:
	errorIndication, errorStatus, errorIndex, varBinds = next(
	    getCmd(SnmpEngine(),
        	   CommunityData('public', mpModel=0),
        	   UdpTransportTarget(('192.168.3.1', 161)),#Address and port
        	   ContextData(),
           		ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.10.5")),#InOctects
           		ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.16.5")),#OutOctects
		 		ObjectType(ObjectIdentity("1.3.6.1.2.1.1.3.0"))#SysUptime
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
			
	time.sleep(how_much_often);
	
	ifInBytes=varBinds[0].prettyPrint().split("= ",1)[1];
	ifOutBytes=varBinds[1].prettyPrint().split("= ",1)[1];
	timeUp=varBinds[2].prettyPrint().split("= ",1)[1];
	
	delta_ifInBytes=float(ifInBytes)-float(old_ifInBytes);
	delta_ifOutBytes=float(ifOutBytes)-float(old_ifOutBytes);
#	delta_old_TimeUp=float(timeUp)-float(old_TimeUp);#Actually is not necessary because I can get periodically
	#It will be useful when the traps are asyncronous
	
	print 'ifspeed: ', if_speed;
	print 'In and out bytes ', ifInBytes, ifOutBytes#, timeUp
	print 'delta values: ', delta_ifInBytes, delta_ifOutBytes#, delta_old_TimeUp
	
	old_ifInBytes=ifInBytes;
	old_ifOutBytes=ifOutBytes;
	#old_TimeUp=timeUp;
	
	utilization=(delta_ifInBytes+delta_ifOutBytes)*8*100/(if_speed*how_much_often);
	print 'The utilization is the ', utilization, '%';
	
	
	
	
	
