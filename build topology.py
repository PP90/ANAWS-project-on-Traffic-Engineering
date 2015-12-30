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

    #build matrix
    for i in range(0, len(listInfo)):
        routes = listInfo[i]['nRoutes']
        for j in range(0, routes):
            draddress = listInfo[i][str(j) + '_draddress']
            k = findDr(draddress, listInfo, i)
            if(k < 0):
                print 'ERROR'
            topologyMatrix[i][k] = listInfo[i][str(j) + '_ip']
    return listInfo, topologyMatrix


def getTopology():
    #output of the command
    output = subprocess.check_output('vtysh -c "show ip ospf database"', shell=True)

    #return the ip list of the routers
    interfaces = decodeTopology(output)

    #return interface list & matrix topology
    interfaceList, matrix = buildTopologyMatrix(interfaces)
    return interfaceList, matrix


#lista, matrice = getTopology()
#print('lista')
#pprint.pprint(lista)
#print('\nmatrice')
#pprint.pprint(matrice)
