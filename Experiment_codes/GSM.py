import numpy as np
from random import random, choice
from igraph import *
import os
import sys
import pandas as pd
from tqdm import tqdm
import utils

# sys.path.append("..")     # for getting utils.py which is located in parent folder
# from utils import *

def h_index(G, node, mode='out'):
    '''
    Return h-index of a node
    '''
    sorted_neighbor_degrees = sorted(G.degree(G.neighbors(node, mode), mode), reverse=True)
    h = 0
    for i in range(1, len(sorted_neighbor_degrees) + 1):
        if sorted_neighbor_degrees[i - 1] < i:
            break
        h = i
    return h

def hi_index(G, node, mode='out'):
    '''
    Return hi_index (h-index on h-index) of a node
    '''
    sorted_neighbor_h_index = sorted([h_index(G, v, mode) for v in G.neighbors(node, mode)], reverse=True)
    h = 0
    for i in range(1, len(sorted_neighbor_h_index) + 1):
        if sorted_neighbor_h_index[i - 1] < i:
            break
        h = i
    return h

def get_cost(G, source_node):
    '''
    Assign costs for each edge
    source_node : igraph Vertex
    '''
    G.vs['h2-idx'] = [hi_index(G, node, 'out') for node in G.vs]
    for node in G.vs:
        if node != source_node:
            dist = len(G.get_shortest_paths(source_node, node, mode='out', output='vpath')[0])
            if dist == 0:
                dist = np.inf
            node['dist'] = dist
            node['cost'] = np.exp(node['dist']) * (node['h2-idx'] - source_node['h2-idx'] + max(G.vs['h2-idx']))


def ICM(graph, seed_nodes):
    '''
    Perform Independent Cascade Model (ICM) for influence spread in a network.

    Parameters:
    - graph: The network graph object (e.g., igraph.Graph) representing the network.
    - seed_nodes: List of seed nodes to initiate the influence spread.

    Returns:
    - activated_nodes: List of nodes that got influenced during the cascade process.
    '''
    activated_nodes = set(seed_nodes)
    queue = seed_nodes.copy()

    while queue:
        current_node = queue.pop(0)
        neighbors = graph.neighbors(current_node)

        for neighbor in neighbors:
            if neighbor not in activated_nodes:
                edge = graph.es.find(_source=current_node, _target=neighbor)
                probability = edge['p']

                if random.random() <= probability:
                    activated_nodes.add(neighbor)
                    queue.append(neighbor)

    return list(activated_nodes)



def get_inf_size(seeds_list):
    inf_size = 0
    inf_list = []
    for seeds in seeds_list:
        inf_size += len(ICM(G, seeds))
        inf_list.append(inf_size / (seeds + 1))
    return inf_size / len(seeds_list)

def get_inf(seeds, no_iterations):
    inf_size = 0
    inf_list = []
    for i in range(no_iterations):
        inf_size += len(ICM(G, seeds))
        inf_list.append(inf_size / (i + 1))
    return inf_size / no_iterations

def GSM(G):
    for source_node in G.vs:
        inf = 0
        for node in G.vs:
            if node != source_node:
                dist = len(G.get_shortest_paths(source_node, node, mode='out', output='vpath')[0])
                if dist == 0:
                    dist = np.inf
                inf += node['shell'] / dist
        source_node['GSM'] = np.exp(source_node['shell'] / len(G.vs)) * inf

def GSM_outdegree(G, source_node):
    for node in G.vs:
        if node != source_node:
            dist = len(G.get_shortest_paths(source_node, node, mode='out', output='vpath')[0])
            if dist == 0:
                dist = np.inf
            node['cost'] = (node.outdegree() + 1) * np.exp(dist)
            node['GSM_outdegree'] = node['GSM'] / node['cost']

def GSM_outdegree_scaled(G, source_node):
    GSM_outdegree(G, source_node)
    max_GSM_outdegree = max(G.vs['GSM_outdegree'])
    for node in G.vs:
        node['GSM_outdegree_scaled'] = node['GSM_outdegree'] / max_GSM_outdegree

def GSM_degree(G, source_node):
    for node in G.vs:
        if node != source_node:
            dist = len(G.get_shortest_paths(source_node, node, mode='out', output='vpath')[0])
            if dist == 0:
                dist = np.inf
            node['cost'] = (node.degree() + 1) * np.exp(dist)
            node['GSM_degree'] = node['GSM'] / node['cost']

def GSM_degree_scaled(G, source_node):
    GSM_degree(G, source_node)
    max_GSM_degree = max(G.vs['GSM_degree'])
    for node in G.vs:
        node['GSM_degree_scaled'] = node['GSM_degree'] / max_GSM_degree

# Set the path to the dataset file
dataset_path = "data/lkml.txt"

def load_graph_data(dataset_path):
    '''
    Load graph data from a dataset file
    '''
    # Read the dataset file and process the data
    # Replace this with your own implementation

    # Example implementation
    graph = Graph.Read(dataset_path)
    shell = [random() for _ in range(len(graph.vs))]

    # Return the graph and shell data
    return {'graph': graph, 'shell': shell}


# Load the dataset
graph_data = load_graph_data(dataset_path)
G = graph_data['graph']
G.vs['shell'] = graph_data['shell']

# Set the number of iterations for influence calculation
no_iterations = 100

# Perform calculations
get_cost(G, G.vs[0])  # Calculate costs using the first node as the source
GSM(G)
GSM_outdegree_scaled(G, G.vs[0])
GSM_degree_scaled(G, G.vs[0])

# Set the seed nodes
seeds = [choice(G.vs) for _ in range(10)]

# Calculate and print the influence size
inf_size = get_inf(seeds, no_iterations)
print("Influence Size:", inf_size)
