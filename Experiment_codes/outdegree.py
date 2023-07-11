import networkx as nx
def out_degree(node, graph):
    """
    Calculate the out-degree of a given node in a graph.

    Parameters:
        node (int): Node ID.
        graph (networkx.Graph): Graph object.

    Returns:
        int: Out-degree of the node.
    """
    return graph.out_degree(node)

# Example usage
G = nx.karate_club_graph()
node_id = 0  # Specify the node ID
degree = out_degree(node_id, G)
print("Out-degree:", degree)
