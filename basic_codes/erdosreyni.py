import networkx as nx
import matplotlib.pyplot as plt 
import random

# G = nx.lollipop_graph(6,10)
# Erdos Reyni Graph G(n,p) : Each edge can exist with probability p (toss a coin; probability of head is p)

#random graph on 1000 nodes
p = 0.5
# G = nx.Graph()
# G.add_nodes_from(range(1,1001))

# for u in range(1,1001):
#     for v in range(1,1001):
#         if (u < v):
#             r = random.uniform(0,1)
#             if (r < p):
#                 G.add_edge(u,v)

G = nx.erdos_renyi_graph(1000,0.5)
print("Number of edges : ",G.number_of_edges())
nx.draw(G,with_labels = True)

plt.show()