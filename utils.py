import numpy as np
from random import random
from igraph import *
import pandas as pd

def ICM_decay(G, start_nodes, decay_fn):
    uninfected = [v for v in G.vs.indices if v not in start_nodes]
    infected = start_nodes.copy()
    active = start_nodes.copy()

    t = 0
    while len(active) != 0 and len(uninfected) != 0:
        reached = []
        for node in active:
            for neighbor in G.neighbors(node, mode='out'):
                if neighbor in uninfected:
                    if random() <= decay_fn(G.es[G.get_eid(node, neighbor)]['p'], t):
                        infected.append(neighbor)
                        reached.append(neighbor)
                        uninfected.remove(neighbor)

        active = reached.copy()
        t += 1
        return infected


def scale(l: list, t_min=0, t_max=1) -> list:
    return (l - np.min(l)) / (np.max(l) - np.min(l)) * (t_max - t_min) + t_min


def compute_prob(G):
    weights = []
    for edge in G.es:
        node = edge.target
        weights.append(1 / (G.degree(node, mode='in') + 0.1))
    return weights


def compute_weighted_prob(G):
    weights = []
    for edge in G.es:
        weights.append(edge["weight"])
    return weights



def compute_cost(G):
    cost = {}
    for node in G.nodes():
        cost[node] = 0

    for edge in G.edges():
        weight = G[edge[0]][edge[1]]['weight']
        cost[edge[0]] += weight
        cost[edge[1]] += weight

    return cost


def read_graph(data_file_path, direct=False, multiple_e=False, weighted=False):
    """
    Read graph from file and remove self-loops, multiple edges, and nodes with zero edges.

    Returns igraph Graph object.
    """

    extension = data_file_path.split('.')[-1]

    if extension == "graphml":
        G = Graph.Read_GraphML(data_file_path, directed=direct)
    elif extension == "txt" or extension == 'edgelist':
        G = Graph.Read_Edgelist(data_file_path, directed=direct)
    elif extension == "csv":
        dataframe = pd.read_csv(data_file_path)
        G = Graph.DataFrame(dataframe, directed=direct)
    else:
        print("Input file format not supported")
        return

    if direct == False:
        print("Converted the graph as directed")
        G.to_directed(mode='mutual')

    if multiple_e == True:
        print("Need to implement multiple edges")
        return
    else:
        G.simplify(loops=True)  # Remove self-loops

    G.delete_vertices(G.vs.select(_degree=0))  # Delete nodes with no edges

    return G

def AA(G: Graph) -> list:
    """
    Returns a list of Adamic Adar Index scores for edges.

    Input:
    G: Igraph Graph object
    """
    prob = []
    for edge in G.es:
        u = edge.source
        v = edge.target
        common_ne = list(set(G.neighbors(u, 'out')).intersection(G.neighbors(v, 'in')))
        score = 0
        for d in G.degree(common_ne, mode='out'):
            score += 1 / (np.log(d + 0.001))
        prob.append(score)
    return prob

def RA(G: Graph) -> list:
    """
    Returns a list of Resource Allocation scores for edges.

    Input:
    G: Igraph Graph object
    """
    prob = []
    for edge in G.es:
        u = edge.source
        v = edge.target
        common_ne = list(set(G.neighbors(u, 'out')).intersection(G.neighbors(v, 'in')))
        score = 0
        for d in G.degree(common_ne, mode='out'):
            score += 1 / d
        prob.append(score)
    return prob

def LHI(G: Graph) -> list:
    """
    Returns a list of Lichtenwalter-Harrell-Newman Index scores for edges.
    """
    prob = []
    for edge in G.es:
        u = edge.source
        v = edge.target
        common_ne = list(set(G.neighbors(u, 'out')).intersection(G.neighbors(v, 'in')))
        prob.append(len(common_ne) / (G.degree(u, mode='out') * G.degree(v, mode='in')))
    return prob

def Jaccard(G: Graph) -> list:
    """
    Returns a list of Jaccard coefficient scores for edges.
    """
    prob = []
    for edge in G.es:
        u = edge.source
        v = edge.target
        common_ne = list(set(G.neighbors(u, 'out')).intersection(G.neighbors(v, 'in')))
        union_ne = list(set(G.neighbors(u, 'out') + G.neighbors(v, 'in')))
        prob.append(len(common_ne) / len(union_ne))
    return prob


def prob_heuristics(G: Graph, method: str) -> list:
    """
    Computes edge probability based on different link prediction heuristics.

    Supported methods: 'AA', 'RA', 'LHI', 'Jaccard'

    Returns a list of edge probabilities.
    """
    if method == 'AA':
        return scale(AA(G))
    elif method == 'RA':
        return scale(RA(G))
    elif method == 'LHI':
        return LHI(G)
    elif method == 'Jaccard':
        return Jaccard(G)

def compute_prob(G):
    weights = []
    for edge in G.es:
        node = edge.target
        weights.append(1 / (G.degree(node, mode='in') + 0.1))
    return weights



def process_graph(data_file_path, direct=False):
    try:
        G = Graph.Read_Edgelist(data_file_path, directed=direct)
    except:
        dataframe = pd.read_csv(data_file_path)
        G = Graph.DataFrame(dataframe, directed=direct)

    if direct == False:
        print("Converted the graph as directed")
        G.to_directed(mode='mutual')

    G.simplify(loops=True)  # remove self loops and combine multiple edges into a single edge

    G.delete_vertices(G.vs.select(_degree=0))  # delete vertices with zero edges

    G.es['p'] = compute_prob(G)  # compute and assign edge probabilities
    G.vs['cost'] = compute_cost(G)  # assign node costs

    return G

def ravi():
    print("working")