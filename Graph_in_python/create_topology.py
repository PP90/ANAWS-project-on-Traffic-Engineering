import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
	G=nx.Graph()

    # add edges
	for edge in graph:
		G.add_edge(edge[0], edge[1])

		# these are different layouts for the network you may try
		# shell seems to work best
	if graph_layout == 'spring':
		graph_pos=nx.spring_layout(G)
	elif graph_layout == 'spectral':
		graph_pos=nx.spectral_layout(G)
	elif graph_layout == 'random':
		graph_pos=nx.random_layout(G)
	else:
		graph_pos=nx.shell_layout(G)

    # draw graph
	nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, alpha=node_alpha, node_color=node_color)
	nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,	alpha=edge_alpha,edge_color=edge_color)
	nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size, font_family=text_font)
	
	nodes_labels=[]
	##TO DO: CREATE A LABEL LIST IN WHICH THERE ARE R1, R2... ROUTERS NAME
	###TO BE CONTINUTED. HAPPY NEW 2016

	print labels
	#nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, label_pos=edge_text_pos)
	nx.draw_networkx_labels(G, graph_pos, labels, font_size=16)
    # show graph
	plt.show()

def get_graph(matrix_topology):
	graph=[]
	for i,element in enumerate(matrix_topology):
			print '\n'
			for j,el in enumerate(element):
				if(el!=0):
					
					print i,' ',j,' ', el
					if(i<j):#In order to avoid	redundancy						
						graph.append((i,j))
	print graph
	return graph



graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9),
         (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]


matrix_topology=[[0, '10.1.1.1', '10.2.2.1', 0, 0, '192.168.3.1'],
 ['10.1.1.2', 0, 0, 0, '10.5.5.1', 0],
 ['10.2.2.2', 0, 0, '10.3.3.1', 0, 0],
 [0, 0, '10.3.3.2', 0, '10.4.4.1', 0],
 [0, '10.5.5.2', 0, '10.4.4.2', 0, 0],
 ['192.168.3.2', 0, 0, 0, 0, 0]] ##HARD CODED MATRIX TOPOLOGY	

my_graph=get_graph(matrix_topology)

draw_graph(my_graph)
