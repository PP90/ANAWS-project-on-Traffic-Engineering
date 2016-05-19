"""
Copyright (c) 2016, Pietro Piscione, Luigi De Bianchi, Giulio Micheloni
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * The names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL P. PISCIONE, L. DE BIANCHI, G. MICHELONI BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
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
