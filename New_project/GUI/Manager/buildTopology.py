import subprocess
#import ipaddress
import re
import pprint
import telnetlib


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
        #If it finds an IPv4 address
        if rule3.search(rows[i]) is not None:
            #Insert it in the listIP
            listIP.append(rule3.search(rows[i]).group())
        #Otherwise, it means that the list of router ip addresses is finished
        else:
            break
    #print(listIP)

    return listIP


def findDr(draddress, listInfo, originalNode):
    for i in range(0, len(listInfo)):
        routes = listInfo[i]['nRoutes']
        for j in range(0, routes):
            if (str(j) + '_draddress') in list(listInfo[i].keys()):
                if(listInfo[i][str(j) + '_draddress'] == draddress):
                    if(i != originalNode):
                        return i
    return -1


def findNextHop(nextHopAddr, listInfo):
    for i in range(0, len(listInfo)):
        if(listInfo[i]['routerId'] == nextHopAddr):
            return i
    return -1


def buildTopologyMatrix(interfaces, ip, mode):
    listInfo = []
    topologyMatrix = [[0 for x in range(len(interfaces))]
                        for x in range(len(interfaces))]

    ruleIP = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    for i in interfaces:
        listInfo.append({})
        listInfo[len(listInfo) - 1]['routerId'] = i
        #cmd = 'vtysh -c "show ip ospf database router ' + i + '"'
        #output = subprocess.check_output(cmd, shell=True)
        cmd = 'show ip ospf database router ' + i + '\n'
        output = ''
        if mode == 'T':
        	cmd = 'show ip ospf database router ' + i + '\n'
        	output = telnetRouter(ip, cmd)
        else:
        	cmd = 'vtysh -c "show ip ospf database router ' + i + '"\n'
        	output = requestToQuagga(cmd)
        rows = output.split('\n')
        #pprint.pprint(rows)

        #find OSPF link
        counter = 0
        for row in range(0, len(rows)):
            #If it is a Transit Network: read the designated router and the incoming interface
            if(re.search('Link connected to: a Transit Network', rows[row]) is not None):
                if(re.search('\(Link ID\) Designated Router address:', rows[row + 1]) is not None):
                    listInfo[len(listInfo) - 1][str(counter) + '_draddress'] = ruleIP.search(rows[row + 1]).group()
                if(re.search('\(Link Data\) Router Interface address:', rows[row + 2]) is not None):
                    listInfo[len(listInfo) - 1][str(counter) + '_ip'] = ruleIP.search(rows[row + 2]).group()
                counter = counter + 1
            #Otherwise checks if it is a point-to-point link
            elif(re.search('Link connected to: another Router \(point-to-point\)', rows[row]) is not None):
                if(re.search('\(Link ID\) Neighboring Router ID:', rows[row + 1]) is not None):
                    listInfo[len(listInfo) - 1][str(counter) + '_nexthopaddr'] = ruleIP.search(rows[row + 1]).group()
                if(re.search('\(Link Data\) Router Interface address:', rows[row + 2]) is not None):
                    listInfo[len(listInfo) - 1][str(counter) + '_ip'] = ruleIP.search(rows[row + 2]).group()
                counter = counter + 1
        listInfo[len(listInfo) - 1]['nRoutes'] = counter
    #pprint.pprint(listInfo)

    #build matrix
    for i in range(0, len(listInfo)):
        routes = listInfo[i]['nRoutes']
        for j in range(0, routes):
            #Looking for the designated router position in the matrix
            if (str(j) + '_draddress') in list(listInfo[i].keys()):
                draddress = listInfo[i][str(j) + '_draddress']
                k = findDr(draddress, listInfo, i)
                if(k < 0):
                    print("ERROR:", draddress, i)
                else:
                    topologyMatrix[i][k] = listInfo[i][str(j) + '_ip']
            else:
                nexthopaddr = listInfo[i][str(j) + '_nexthopaddr']
                k = findNextHop(nexthopaddr, listInfo)
                if(k < 0):
                    print("ERROR:", draddress, i)
                else:
                    topologyMatrix[i][k] = listInfo[i][str(j) + '_ip']

    return listInfo, topologyMatrix

def telnetRouter(ipaddr, cmd):
    tn = telnetlib.Telnet(ipaddr)
    tn.write(cmd)
    output = tn.read_until('>')
    output = tn.read_until('>')
    tn.close
    return output
    
def requestToQuagga(cmd):
	output = subprocess.check_output(cmd, shell=True)
	return output

def getTopology(ip, mode):
    output = None
    if mode == 'Q':
        #output of the command
        output = subprocess.check_output('vtysh -c "show ip ospf database"', shell=True)
    else:
        output = telnetRouter(ip, 'show ip ospf database\n')
    if output == None:
        return None, None
    #return the ip list of the routers
    interfaces = decodeTopology(output)

    #return interface list & matrix topology
    interfaceList, matrix = buildTopologyMatrix(interfaces, ip, mode)
    return interfaceList, matrix


#lista, matrice = getTopology('192.168.3.1', 'T')
#if(lista == None):
    #print("Some error")
#print('lista')
#pprint.pprint(lista)
#print('\nmatrice')
#pprint.pprint(matrice)
