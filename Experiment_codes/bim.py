import networkx as nx
import random

def calculate_influence(seed, graph, iterations):
    # Calculate the influence spread of a seed node using the independent cascade model

    # Initialize the activated nodes with the seed node
    activated = set([seed])
    newly_activated = set([seed])

    # Perform the influence propagation for the specified number of iterations
    for i in range(iterations):
        # Iterate over the newly activated nodes in the previous iteration
        # and activate their neighbors with a certain probability
        neighbors = set()
        for node in newly_activated:
            neighbors.update(graph.neighbors(node))
        for node in neighbors:
            if node not in activated:
                # Activate the neighbor with a certain probability (e.g., 0.1)
                probability = 0.1
                if random.random() <= probability:
                    activated.add(node)
        newly_activated = neighbors

    # Calculate the influence spread as the number of activated nodes
    influence_spread = len(activated)

    return influence_spread

def calculate_cost(seed, source, graph):
    # Calculate the cost of selecting a seed node based on the proposed cost function

    # Calculate the distance between the seed and source node using the shortest path
    distance = nx.shortest_path_length(graph, source, seed)

    # Calculate the outdegree of the seed node
    outdegree = graph.out_degree(seed)

    # Calculate the cost using the proposed cost function
    cost = distance * outdegree * len(graph) / sum(graph.out_degree(node) for node in graph)

    return cost

# Example usage
if __name__ == "__main__":
    # Load your graph from a real-world dataset or construct it using other methods
    G = nx.karate_club_graph()

    # Define the source node and a seed node
    source = 0
    seed = 33

    # Set the number of iterations for influence propagation
    iterations = 100

    # Calculate the influence spread for the seed node
    influence_spread = calculate_influence(33, G, iterations)

    # Calculate the cost for the seed node
    cost = calculate_cost(33, 0, G)

    # Print the calculated influence spread and cost
    print("Influence Spread:", influence_spread)
    print("Cost:", cost)
