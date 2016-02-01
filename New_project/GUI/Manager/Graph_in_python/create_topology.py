import networkx as nx
import matplotlib.pyplot as plt


THRESHOLD_GREEN=25
THRESHOLD_RED=75
WHITE_COLOR='#FFFFFF'
YES_TUNNELING=1
NO_TUNNELING=0
YES_PLOT=1
NO_PLOT=0

##Not used yet.
##Giving as parameter the graph and the list of the link not in tunnel, this fuction returns the graph with only tunnel links.
##The arches removed are those not present in the tunnel. This functionality is not completed yet.
def remove_not_tunnel_links(graph, not_tunnel_links):
	#print graph
	#print not_tunnel_links
	for link in not_tunnel_links:
			for edge in graph:
				if(link==edge):
					graph.remove(edge)				
	return graph


##This fuction plots the network topology and possibly the links utilizations. It returns the graph with the arches removed. 
def build_graph(graph, matrix_topology, interfaces_names=None, color_vector=None, plot=YES_PLOT):

    # create networkx graph
	G=nx.Graph()
	tunneling=NO_TUNNELING

	if(tunneling):
		graph=remove_not_tunnel_links( graph, not_tunnel_links)
		print 'After updating: ',graph	

	  # add edges
	for edge in graph:
		G.add_edge(edge[0], edge[1])
		
	if(plot==YES_PLOT):
		show_graph(G, graph, interfaces_names, color_vector)
	else:
		return plt

##This function shows the graph.
def show_graph(G, graph, interfaces_names, color_vector, labels=None, graph_layout='spectral', node_size=600, node_color='blue',node_alpha=0.5,node_text_size=4, edge_color='blue', edge_alpha=0.9, edge_tickness=6, edge_text_pos=0.25, text_font='sans-serif'):

		##defining the layout
	if graph_layout == 'spring':
		graph_pos=nx.spring_layout(G)
	elif graph_layout == 'spectral':
		graph_pos=nx.spectral_layout(G)
	else:
		graph_pos=nx.shell_layout(G)

  	#Bindings the nodes
	labels={}
	for idx, node in enumerate(G.nodes()):
		hostname='R'+str(idx+1)
		labels[idx]=hostname
	
	nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, alpha=node_alpha, node_color=node_color)
	
	#Drawing the edges
	if(color_vector!=None):
		nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,	alpha=edge_alpha,edge_color=color_vector)
	else:
		nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,	alpha=edge_alpha,edge_color=WHITE_COLOR)

	##draw network edges labels and nodes label
	if(interfaces_names!=None):
		edge_labels=dict(zip(graph, interfaces_names))
		nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, label_pos=edge_text_pos, bbox=dict(facecolor='none',edgecolor='none'))	

	nx.draw_networkx_labels(G, graph_pos, labels, font_size=16)
   	plt.axis('off')
	plot_title='Network topology'

	if(color_vector!=None):
		plot_title=plot_title+' and utilization'
	
	plt.title(plot_title)
	plt.show()


##This function returns the graph as a list of connections among the network nodes and the interface list
def get_graph_and_arches(matrix_topology, matrix_interfaces = None):
	graph=[]
	interfaces_list=[]
	for i,element in enumerate(matrix_topology):
		for j,el in enumerate(element):
			if(el!=0):
				#print i,' ',j,' ', el						
				graph.append((i,j))
				if matrix_interfaces != None:
					interfaces_list.append(matrix_interfaces[i][j])
	#print graph, 
	#print interfaces_list
	return graph, interfaces_list


def interfaces_list(matrix_interfaces):
	interfaces_list=[]
	if matrix_interfaces == None:
		return interfaces_list
	for interface in matrix_interfaces:
		if (interface!='0'):
			interfaces_list.append(interface)
	return interfaces_list

##Giving in input the matrix utilizations, this fuction returns the color vector. The color vector consists of of an list in which there are many elements how many are the edge in the graph. The element are the corresponding utilization expressed from green to red encoding as follow in color_shades vector.
def get_color_vector(matrix_utilization):
	color_vector=[]
	color_shades=['#2FFF91','#11FF00','#22FF00','#33FF00','#44FF00','#55FF00','#66FF00','#77FF00','#88FF00','#99FF00',
'#AAFF00','#BBFF00','#CCFF00','#DDFF00','#EEFF00','#FFFF00','#FFEE00','#FFDD00','#FFCC00','#FFBB00',
'#FFAA00','#FFAA00','#FF9900','#FF8800','#FF7700','#FF6600','#FF5500','#FF4400','#FF3300','#FF2200',
'#FF1100','#FF0000','#FF0000','#FF0000']
	green_threshold=THRESHOLD_GREEN
	red_threshold=THRESHOLD_RED
	for i,row in enumerate(matrix_utilization):
		for j, element in enumerate(row):
			if (j>i):
				element=int(element)
				if element!=-1:
					element=(matrix_utilization[i][j]+matrix_utilization[j][i])/2
					##The matrix utilization can be asymmetric.
					##A link can be connected to two interfaces. Such interfaces can have different utilizations.
					##The utilization on the link will be averaged
					index=element/3
					color_vector.append(color_shades[index])
	return color_vector
	
def get_arches_to_delete(matrix_topology, tunnel_topology):
	edge_to_delete=[]
	for i,row in enumerate(matrix_topology):
		for j,element in enumerate(row):
			if(element!=tunnel_topology[i][j]):
				to_add=(i,j)
				edge_to_delete.append(to_add)

	return edge_to_delete

tunnel_topology=[[0, 0, 0, 0, 0, '192.168.3.1'],
 [0, 0, 0, 0, 0, 0],
 ['10.2.2.2', 0, 0, '10.3.3.1', 0, 0],
 [0, 0, '10.3.3.2', 0, '10.4.4.1', 0],
 [0, 0, 0, '10.4.4.2', 0, 0],
 ['192.168.3.2', 0, 0, 0, 0, 0]] ##HARD CODED MATRIX TOPOLOGY	


tunnel_interfaces=[[0, 0, 'FA10', 0, 0, 'ETH20'],
 [0, 0, 0, 0, 0, 0],
 ['FA00', 0, 0, 'FA10', 0, 0],
 [0, 0, 'FA00', 0, 'FA10', 0],
 [0, 0, 0, 'FA10', 0, 0],
 ['ETH20', 0, 0, 0, 0, 0]] ##HARD CODED INTERFACES MATRIX	


####
matrix_topology=[[0, '10.1.1.1', '10.2.2.1', 0, 0, '192.168.3.1'],
 ['10.1.1.2', 0, 0, 0, '10.5.5.1', 0],
 ['10.2.2.2', 0, 0, '10.3.3.1', 0, 0],
 [0, 0, '10.3.3.2', 0, '10.4.4.1', 0],
 [0, '10.5.5.2', 0, '10.4.4.2', 0, 0],
 ['192.168.3.2', 0, 0, 0, 0, 0]] ##HARD CODED MATRIX TOPOLOGY	


matrix_interfaces=[[0, 'FA00', 'FA10', 0, 0, 'ETH20'],
 ['FA00', 0, 0, 0, 'FA10', 0],
 ['FA00', 0, 0, 'FA10', 0, 0],
 [0, 0, 'FA00', 0, 'FA10', 0],
 [0, 'FA00', 0, 'FA10', 0, 0],
 ['ETH20', 0, 0, 0, 0, 0]] ##HARD CODED INTERFACES MATRIX	



matrix_utilization=[[-1, 20, 100, -1, -1, 100],
 [20, -1, -1, -1, 80, -1],
 [30, -1, -1, 55, -1, -1],
 [-1, -1, 55, -1, 20, -1],
 [-1, 80, -1, 20, -1, -1],
 [40, -1, -1, -1, -1, -1]] ##HARD CODED MATRIX UTILIZATION. IT IS ALWAYS NxN where N is the number of the router in the network.

def main():
	#All topology
	links_not_in_tunnel=get_arches_to_delete(matrix_topology, tunnel_topology)
	my_graph, interfaces_names=get_graph_and_arches(matrix_topology)
	build_graph(my_graph, matrix_topology)
