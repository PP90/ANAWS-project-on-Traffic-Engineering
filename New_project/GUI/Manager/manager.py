import buildTopology
import re
from Mpls_snmp import *
from SNMP_utilization_src import *

#####################################
#find method are for private use
#get method are for public call
#####################################


class Manager:

    def __init__(self, anchorIp, cs):
        #main
        self.anchorIp = anchorIp
        self.communityString = cs

        #topology
        self.topologyMatrix = None
        self.listInfo = None

        #utilization

        #tunnel
        #key search are ip
        self.confTunnelsDictionary = {}
        self.lspTableDictionary = {}

    ###############UTILITY
    def returnIndex(self, addr):
        for k in range(0, len(self.listInfo)):
            if self.listInfo[k]['routerId'] == addr:
                return k
        return None

    def returnRouter(self, ip):
        ruleIP = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        temp = ruleIP.search(ip).group()

        #search in listInfo
        for i in list(self.listInfo):
            for j in range(0, i['nRoutes']):
                if i[str(j) + '_ip'] == temp:
                    return i['routerId']

    def removeDuplicates(self, values):
        output = []
        seen = set()
        for value in values:
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output


    ###############TOPOLOGY
    def findTopology(self):
        """find topology and save list of routers and matrix"""
        self.listInfo, self.topologyMatrix = buildTopology.getTopology(self.anchorIp)

    def getListIP(self):
        """return list of ip if not present call function to populate data"""
        listIp = []
        if self.listInfo is None:
            #unallocated memory call find function
            self.findTopology()
        for i in range(0, len(self.listInfo)):
            listIp.append(self.listInfo[i]['routerId'])
        return listIp

    def getTopology(self):
        """return topology if not present call function to populate data"""
        if self.topologyMatrix is None:
            #unallocated memory call find function
            self.findTopology()
        return self.topologyMatrix

    ###############UTILIZATION
    def getRoutersList(self, addrList):
        return getRouterInfo.get_routers_list(addrList, self.communityString)


    def findUtilization(self, addr):
        """if the output is None some error occurred"""
        index = self.returnIndex(addr)
        if index is None:
            return None

        a = []
        a.append(addr)
        r = getRouterInfo.get_routers_list(a, self.communityString)
        ifs = r[0].get_interfaces()
        for i in range(0, len(ifs)):
            ip = ifs[i].get_address_if()
            for j in range(0, self.listInfo[index]['nRoutes']):
                if ip == self.listInfo[index][str(j) + '_ip']:
                    #match
                    #add new info
                    self.listInfo[index][str(j) + '_name'] = ifs[i].get_name()
                    self.listInfo[index][str(j) + '_id'] = ifs[i].get_id()
                    self.listInfo[index][str(j) + '_speed'] = ifs[i].get_if_speed()
                    self.listInfo[index][str(j) + '_utilization'] = ifs[i].get_in_out_utilization()
        #no statefull meaning only to have an output different from None
        return 1

    def getUtilization(self, addr):
        """return utilization for the current ip if return None some error occurred"""
        if self.listInfo is None:
            self.findTopology()
            res = self.findUtilization(addr)
            if res is None:
                return None

        index = self.returnIndex(addr)
        if index is None:
            return None

        if ('0_name') not in list(self.listInfo[index].keys()):
            #it's only needed to test if one name is present
            res = self.findUtilization(addr)
            if res is None:
                return None

        return self.listInfo[index]
    #def getAllUtilization():

    ###############TUNNEL
    def findTunnel(self, ip):
        t = TeTunnels.TeTunnels(ip, self.communityString)
        t.start()

        self.confTunnelsDictionary[ip] = t.getConfTunnels()
        self.lspTableDictionary[ip] = t.getLspTable()

        #for name in confTunnels.keys():
            #print name, confTunnels[name].getAttributeDict()

    def getTunnel(self, ip):
        if (ip in self.confTunnelsDictionary or ip in self.lspTableDictionary) is False:
            self.findTunnel(ip)

        results = []
        for name in list(self.lspTableDictionary[ip].keys()):
            attributes = self.lspTableDictionary[ip][name].getAttributeDict()
            if attributes['mplsTunnelRole'] == '1':
                results.append(attributes['Computed Path'])

        #compute router path
        for i in range(0, len(results)):
            #add ip as origin
            results[i].insert(0, ip)
            #delete last element
            results[i].pop()
            for j in range(1, len(results[i])):
                k = results[i][j]
                results[i][j] = self.returnRouter(k)
        #remove duplicates
        for i in range(0, len(results)):
            results[i] = self.removeDuplicates(results[i])
        return results