import buildTopology

#from Mpls_snmp.TeTunnels import *
#from Mpls_snmp.Container import *
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


    ###############UTILIZATION
    def findUtilization():


    def getUtilization():
    def getAllUtilization():


        """return topology if not present call function to populate data"""
        if self.topologyMatrix is None:
            #unallocated memory call find function
            self.findTopology()
        return self.topologyMatrix

    ###############OCCUPATION
    #def findOccuption(ip):

    #def getOccupation(ip, interface):

    #def getAllOccupation():

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