import networkx as nx
import random

def calculate_influence(node, seed_set, graph):
    # Perform influence propagation calculation for a given node and seed set
    # Implement the influence propagation using the Independent Cascade model

    active_nodes = seed_set.copy()
    influenced_nodes = set()
    influenced_nodes.add(node)

    while active_nodes:
        new_active_nodes = set()
        for seed in active_nodes:
            neighbors = set(graph.neighbors(seed))
            neighbors.difference_update(seed_set)
            for neighbor in neighbors:
                if neighbor not in influenced_nodes:
                    # Determine if the neighbor gets influenced based on edge probabilities
                    influence_prob = graph.edges[seed, neighbor]['weight']
                    if random.random() <= influence_prob:
                        influenced_nodes.add(neighbor)
                        new_active_nodes.add(neighbor)

        active_nodes = new_active_nodes

    influence = len(influenced_nodes) - len(seed_set)  # Influence is the number of newly influenced nodes
    return influence

def calculate_cost(seed, source, graph):
    # Calculate the cost of selecting a seed node based on the proposed cost function

    # Calculate the distance between the seed and source node using the shortest path
    distance = nx.shortest_path_length(graph, source, seed)

    # Calculate the outdegree of the seed node
    outdegree = graph.out_degree(seed)

    # Calculate the cost using the proposed cost function
    cost = distance * outdegree * len(graph) / sum(graph.out_degree(node) for node in graph)

    return cost


# Calculating the BIM using greedy Algorithm
def greedy_bim(graph, k, source, budget):
    seed_set = set()
    cost = 0

    while len(seed_set) < k and cost <= budget:
        candidate_nodes = set(graph.nodes()) - seed_set
        candidate_costs = {node: calculate_cost(node, source, graph) for node in candidate_nodes}
        sorted_candidates = sorted(candidate_costs, key=lambda x: candidate_costs[x])

        for node in sorted_candidates:
            if cost + candidate_costs[node] <= budget:
                seed_set.add(node)
                cost += candidate_costs[node]
        
        # Perform influence calculation for the newly added seed nodes
        for seed in seed_set:
            influence = calculate_influence(seed, seed_set, graph)
            # Use the influence value as needed, e.g., for evaluation or further processing

    return seed_set



# Example usage
# Load your graph from a real-world dataset or construct it using other methods
G = nx.karate_club_graph()

# Define the number of seeds to be chosen, source node, and budget
k = 5
source = "SourceNode"
budget = 10

# Generate random edge probabilities for the graph
for edge in G.edges():
    G.edges[edge]['weight'] = random.random()

# Run the BIM algorithm
selected_seeds = greedy_bim(G, k, source, budget)

# Print the selected seed nodes
print("Selected seeds:", selected_seeds)
