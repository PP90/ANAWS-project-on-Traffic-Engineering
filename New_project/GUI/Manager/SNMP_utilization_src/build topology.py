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
import subprocess
#import ipaddress
import re
import pprint


def decodeTopology(output):
    #var
    startRow = 0
    listIP = []

    #regular expression
    rule1 = re.compile('Router Link States')
    rule2 = re.compile('Link ID')
    rule3 = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    #divide it in rows
    rows = output.split('\n')

    #search for "Router Link States"
    for i in range(0, len(rows)):
        if rule1.search(rows[i]) is None:
            continue
        else:
            startRow = i
            break
    #print(startRow)

    #search for "Link ID "
    for i in range(startRow, len(rows)):
        if rule2.search(rows[i]) is None:
            continue
        else:
            #return i+1 because the first usable results is in the next line
            startRow = (i + 1)
            break
    #startRow is the row of the first ip
    #print(startRow)

    #we only need the first ip of each line
    #search for "ip" until empty line
    for i in range(startRow, len(rows)):
        if(len(rows[i]) == 0):
            #empty line found
            break
        listIP.append(rule3.search(rows[i]).group())
    #print(listIP)

    return listIP


def findDr(draddress, listInfo, originalNode):
    for i in range(0, len(listInfo)):
        routes = listInfo[i]['nRoutes']
        for j in range(0, routes):
            if(listInfo[i][str(j) + '_draddress'] == draddress):
                if(i != originalNode):
                    return i
    return -1


def buildTopologyMatrix(interfaces):
    listInfo = []
    topologyMatrix = [[0 for x in range(len(interfaces))]
                        for x in range(len(interfaces))]

    ruleIP = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    for i in interfaces:
        listInfo.append({})
        listInfo[len(listInfo) - 1]['routerId'] = i
        cmd = 'vtysh -c "show ip ospf database router ' + i + '"'
        output = subprocess.check_output(cmd, shell=True)
        rows = output.split('\n')
        #pprint.pprint(rows)

        #find OSPF link
        counter = 0
        for row in range(0, len(rows)):
            if(re.search('Link connected to: a Transit Network', rows[row]) is not None):
                if(re.search('\(Link ID\) Designated Router address:', rows[row + 1]) is not None):
                    listInfo[len(listInfo) - 1][str(counter) + '_draddress'] = ruleIP.search(rows[row + 1]).group()
                if(re.search('\(Link Data\) Router Interface address:', rows[row + 2]) is not None):
                    listInfo[len(listInfo) - 1][str(counter) + '_ip'] = ruleIP.search(rows[row + 2]).group()
                counter = counter + 1
        listInfo[len(listInfo) - 1]['nRoutes'] = counter

    #pprint.pprint(listInfo)
    for i in range(0, len(listInfo)):
        routes = listInfo[i]['nRoutes']
        for j in range(0, routes):
            draddress = listInfo[i][str(j) + '_draddress']
            k = findDr(draddress, listInfo, i)
            if(k < 0):
                print 'ERROR'
            topologyMatrix[i][k] = listInfo[i][str(j) + '_ip']
    return topologyMatrix


output = subprocess.check_output('vtysh -c "show ip ospf database"', shell=True)
interfaces = decodeTopology(output)
print(interfaces)
matrix = buildTopologyMatrix(interfaces)
print(matrix)