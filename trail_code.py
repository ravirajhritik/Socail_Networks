import igraph as ig
import random

def ICM_decay(graph, seed_set, decay_fn=lambda p, t: p):
    activated_nodes = set(seed_set)
    activated_edges = set()

    for node in seed_set:
        for neighbor in graph.neighbors(node):
            if graph.are_connected(node, neighbor):
                activated_edges.add((node, neighbor))

    t = 0
    while activated_edges:
        newly_activated_nodes = set()
        newly_activated_edges = set()

        for edge in activated_edges:
            node, neighbor = edge
            weight = graph.es[graph.get_eid(node, neighbor)]['weight']
            if random.random() <= decay_fn(weight, t):
                newly_activated_nodes.add(neighbor)
                for new_neighbor in graph.neighbors(neighbor):
                    if graph.are_connected(neighbor, new_neighbor):
                        newly_activated_edges.add((neighbor, new_neighbor))

        activated_nodes |= newly_activated_nodes
        activated_edges = newly_activated_edges - activated_edges
        t += 1

    return activated_nodes


def BIM(graph, budget, method, num_iterations):
    seed_set = []
    for _ in range(num_iterations):
        candidate_seed_set = []
        candidate_node_scores = []
        for node in graph.vs:
            if node['cost'] <= budget:
                candidate_seed_set.append(node.index)
                if method == 'random':
                    candidate_node_scores.append(random.random())

        if not candidate_seed_set:
            break

        influenced_nodes = ICM_decay(graph, candidate_seed_set)
        influence = len(influenced_nodes)
        max_score = max(candidate_node_scores)

        if method == 'random':
            indices = [i for i, score in enumerate(candidate_node_scores) if score == max_score]
            selected_index = random.choice(indices)
            selected_node = candidate_seed_set[selected_index]
            seed_set.append(selected_node)
            budget -= graph.vs[selected_node]['cost']

    return seed_set

def main():
    graph_file = "dolphins.txt"
    budget = 10
    method = 'random'
    num_iterations = 100

    # Load graph
    graph = ig.Graph.Read_Edgelist(graph_file, directed=False)

    # print(graph.es['weight'])
    # print(graph.vs['cost'] )

    # Set default attributes if missing
    if 'weight' not in graph.edge_attributes():
        graph.es['weight'] = 1
    if 'cost' not in graph.vs.attributes():
        graph.vs['cost'] = 1

    # Convert the graph to a directed graph
    if not graph.is_directed():
        graph = graph.as_directed()

    print("Converted the graph as directed")

    # Run BIM algorithm
    seed_set = BIM(graph, budget, method, num_iterations)
    print("Seed Set:", seed_set)

if __name__ == "__main__":
    main()
