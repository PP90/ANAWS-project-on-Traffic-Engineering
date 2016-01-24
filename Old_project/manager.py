import buildTopology
#import Mpls_snmp
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
    def findUtilization(self, addr):
        """if the output is None some error occurred"""
        index = None
        for k in range(0, len(self.listInfo)):
            if self.listInfo[k]['routerId'] == addr:
                index = k
        if index is None:
            return None
        #print(index)
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




    #def getUtilization():
    #def getAllUtilization():


    ###############TUNNEL
    #def findTunnel(ip, communityString):
        #t = TeTunnels(ip, communityString)
        #t.start()

        #self.confTunnelsDictionary[ip] = t.getConfTunnels()
        #self.lspTableDictionary[ip] = t.getLspTable()

        ##For each tunnel configuration:
        ##for name in confTunnels.keys():
        ##    print name, confTunnels[name].getAttributeDict()

        ##For each LSP instance
        ##for name in Lsp.keys():
        ##    print name, Lsp[name].getAttributeDict()

    #def getTunnel(ip, communityString):
        #if (self.confTunnelsDictionary.has_key(ip) or self.lspTableDictionary.has_key(ip)) is False:
            #findTunnel(ip, communityString)
        #return self.confTunnelsDictionary[ip], self.lspTableDictionary[ip]



    ###############GRAPH
    #def getGraph():