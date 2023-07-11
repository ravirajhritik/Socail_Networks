import networkx as nx
import matplotlib as plt

G=nx. read_edgelist("facebook_combined.txt")
print(nx.transitivity(G))