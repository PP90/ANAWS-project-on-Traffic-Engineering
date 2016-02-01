import buildTopology
import re
from Mpls_snmp import *
from SNMP_utilization_src import *
from Graph_in_python.create_topology import *
import threading


#####################################
#find method are for private use
#get method are for public call
#####################################


class Manager:

    def __init__(self, anchorIp, cs, mode, guiReference):
        #main
        self.anchorIp = anchorIp
        self.communityString = cs
        self.mode = mode
        self.guiReference = guiReference

        #topology
        self.topologyMatrix = None
        self.listInfo = None

        #utilization
        self.routersList = None
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

    def returnNameIndex(self, index, name):
        for i in range(0, self.listInfo[index]['nRoutes']):
            if name == self.listInfo[index][str(i) + '_name']:
                return i
        return None

    ###############TOPOLOGY
    def findTopology(self):
        """find topology and save list of routers and matrix"""
        self.listInfo, self.topologyMatrix = buildTopology.getTopology(self.anchorIp, self.mode)

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

    def getGraph(self, topologyMatrix, matrix_interfaces = None):
        my_graph, interfaces_names = get_graph_and_arches(topologyMatrix, matrix_interfaces)
        return build_graph(my_graph, topologyMatrix, interfaces_names)

    ###############UTILIZATION
    def getRoutersList(self, addrList):
        self.routersList = getRouterInfo.get_routers_list(addrList, self.communityString)
        return self.routersList

    def findRouterObjFromAddr(self, addr):
        if self.routersList is not None:
            for router in self.routersList:
                if addr == router.get_address():
                    return router
        return None

    def findUtilization(self, addr):
        """if the output is None some error occurred"""
        index = self.returnIndex(addr)
        if index is None:
            return None

        #Avoid to waste time in retrieving information already taken
        router = []
        router.append(self.findRouterObjFromAddr(addr))
        if router[0] is None:
            a = []
            a.append(addr)
            router = self.getRoutersList(a)

        ifs = router[0].get_interfaces()
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

        my_router = getRouterInfo.get_utilization_single_router_polling(router, self.communityString)
        #my_router.print_ifs_utilization()
        for interface in my_router.get_interfaces():
            i = self.returnNameIndex(index, interface.get_name())
            if i is not None:
                self.listInfo[index][str(i) + '_utilization'] = interface.get_in_out_utilization()
            #else:
                #interface not in ospf

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

        #output is a dictionary {interfaceName : utilization}
        output = {}
        for i in range(0, self.listInfo[index]['nRoutes']):
            output[self.listInfo[index][str(i) + '_name']] = []
            output[self.listInfo[index][str(i) + '_name']].append(self.listInfo[index][str(i) + '_utilization'])
            output[self.listInfo[index][str(i) + '_name']].append(self.listInfo[index][str(i) + '_speed'])
        return output

    def getAllUtilization(self, addrList, refresh=False):
        result = {}
        for addr in addrList:
            if refresh is True:
                self.findUtilization(addr)
            output = self.getUtilization(addr)
            routerObj = self.findRouterObjFromAddr(addr)
            if routerObj is not None:
                result[routerObj.get_hostname()] = output
        return result

    ###############TUNNEL
    def findTunnel(self, ip):
        t = TeTunnels.TeTunnels(ip, self.communityString)
        t.start()

        self.confTunnelsDictionary[ip] = t.getConfTunnels()
        self.lspTableDictionary[ip] = t.getLspTable()

        #for name in confTunnels.keys():
            #print name, confTunnels[name].getAttributeDict()

    def getTunnel(self, ip):
        """return the list of traversed router"""
        #this is needed cause we need listInfo
        if self.listInfo is None:
            self.findTopology()

        if (ip in self.confTunnelsDictionary or ip in self.lspTableDictionary) is False:
            self.findTunnel(ip)

        results = {}
        for name in list(self.lspTableDictionary[ip].keys()):
            attributes = self.lspTableDictionary[ip][name].getAttributeDict()
            if attributes['mplsTunnelRole'] == '1':
                results[name] = attributes['Computed Path']
        #compute router path
        for i in results:
            #add ip as origin
            results[i].insert(0, ip)
            #delete last element
            results[i].pop()
            for j in range(1, len(results[i])):
                k = results[i][j]
                results[i][j] = self.returnRouter(k)
        #remove duplicates
        for i in results:
            results[i] = self.removeDuplicates(results[i])
        return results

    def getAllTunnels(self, ip):
        if self.listInfo is None:
            self.findTopology()
        if (ip in self.confTunnelsDictionary or ip in self.lspTableDictionary) is False:
            self.findTunnel(ip)
        return self.lspTableDictionary[ip]

    ###############GUI
    def setUtilizationToGui(self, timer, addr):
        self.findUtilization(addr)
        result = self.getUtilization(addr)
        self.guiReference.setUtilization(result)
        threading.Timer(timer, self.setUtilizationToGui, [timer, addr]).start()
        return

    def startThreads(self, reruntime, addr):
        threading.Thread(target=self.setUtilizationToGui, args=(reruntime, addr, )).start()

    def stopThreads(self):
        for t in threading.enumerate():
            if t.__class__.__name__ != '_MainThread':
                t.cancel()