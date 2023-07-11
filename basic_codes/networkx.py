import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph() #0 nodes, 0 edges

# G.add_edge(0,1) nodes are not existing ; so creates the nodes and adds edge 0 --> 1

for i in range(1,100):
    G.add_edge(i,i+1)

nx.draw(G,with_labels = True,node_color = 'red')

plt.show()