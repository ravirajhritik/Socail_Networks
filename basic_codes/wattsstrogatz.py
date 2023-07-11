import os 
import networkx as nx
import matplotlib.pyplot as plt

G_R = nx.watts_strogatz_graph(4039,40,0.2)
G_J = nx.karate_club_graph()
G_Real = nx.read_edgelist(os.path.join(os.pardir,"data","facebook_combined.txt"))

# print(G_J.nodes)
no_nodes = G_J.number_of_nodes()
no_edges = G_J.number_of_edges()

G_Rand = nx.gnm_random_graph(no_nodes,no_edges)

#clustering/transitivity = no of closed triangles/triads a->b a->c triad = 1 if a->c ==> closed triangle = 1 so trans = 1

# print("Karate : ",nx.transitivity(G_J),nx.average_shortest_path_length(G_J))
# print("Random : ",nx.transitivity(G_Rand),nx.average_shortest_path_length(G_Rand))
print("FB : ",nx.transitivity(G_Real),nx.average_shortest_path_length(G_Real))

# print("EDGES : ",G_R.number_of_edges())
print("Watts Strogatz  : ",nx.transitivity(G_R), nx.average_shortest_path_length(G_R))
#check if it follows six degree of separation