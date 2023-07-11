import networkx as nx
import matplotlib.pyplot as plt
import os

G_J = nx.karate_club_graph()

# print(G_J.nodes)
no_nodes = G_J.number_of_nodes()
no_edges = G_J.number_of_edges()

G_R = nx.gnm_random_graph(no_nodes,no_edges)

#clustering/transitivity = no of closed triangles/triads a->b a->c triad = 1 if a->c ==> closed triangle = 1 so trans = 1

print("Karate : ",nx.transitivity(G_J))
print("Random : ",nx.transitivity(G_R))

# G_T = nx.read_edgelist(os.path.join(os.pardir,"higgs-social_network.edgelist"))

# # print("Twitter followers : ",nx.transitivity(G_T))
# print(G_T.number_of_nodes(),G_T.number_of_edges())
