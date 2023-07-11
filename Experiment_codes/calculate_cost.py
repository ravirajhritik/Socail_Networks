import networkx as nx
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
# Load your graph from a real-world dataset or construct it using other methods
G = nx.karate_club_graph()

# Define the source node and a seed node
source = "SourceNode"
seed = "SeedNode"

# Calculate the cost for the seed node
cost = calculate_cost(seed, source, G)

# Print the calculated cost
print("Cost:", cost)
