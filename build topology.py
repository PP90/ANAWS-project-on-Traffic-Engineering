import subprocess
#import ipaddress
import re

def decodeTopology(output):
    #variabili
    startRow = 0
    listIP = []

    #divide it in rows
    rows = output.split('\n')
    #regular expression
    rule1 = re.compile('Router Link States')
    rule2 = re.compile('Link ID')
    rule3 = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

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
    #search for "ip ip " until empty line
    for i in range(startRow, len(rows)):
        if(len(rows[i]) == 0):
            #empty line found
            break
        listIP.append(rule3.search(rows[i]).group())
    #print(listIP)

    return listIP





output = subprocess.check_output('vtysh -c "show ip ospf database"', shell = True)
decodeTopology(output)


