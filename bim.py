import os
from random import random
import pandas as pd
from tqdm import tqdm
from igraph import *
from utils import *
import utils


def BIM(G, budget, method='AA', num_iterations=100):
    # Initialize variables
    seed_set = []
    max_influence = 0

    for _ in tqdm(range(num_iterations), desc="Running BIM"):
        current_budget = budget
        current_seed_set = []
        current_influence = 0

        # Iteratively select nodes until the budget is exhausted
        while current_budget > 0:
            # Compute probabilities based on the selected method
            probabilities = prob_heuristics(G, method)

            # Calculate the expected influence for each candidate node
            candidate_influences = []
            for v in range(G.vcount()):
                if v not in current_seed_set:
                    candidate_seed_set = current_seed_set + [v]
                    influenced_nodes = ICM_decay(G, candidate_seed_set, decay_fn=lambda p, t: p)
                    candidate_influence = len(influenced_nodes)
                    candidate_influences.append(candidate_influence)
                else:
                    candidate_influences.append(0)

            # Find the node with the highest expected influence
            max_influence_node = np.argmax(candidate_influences)
            max_influence_value = candidate_influences[max_influence_node]

            # If the maximum influence is zero or the budget is exhausted, break the loop
            if max_influence_value == 0 or current_budget == 0:
                break

            # Update the seed set, influence, and budget
            current_seed_set.append(max_influence_node)
            current_influence += max_influence_value
            current_budget -= G.vs[max_influence_node]['cost']

        # Update the seed set and maximum influence if the current influence is higher
        if current_influence > max_influence:
            max_influence = current_influence
            seed_set = current_seed_set

    return seed_set


def main():
    # Set the path to the graph network data file
    data_file_path = "dolphins.txt"
    # data_file_path = "facebook_combined.txt"

    # Read the graph from the data file
    G = utils.read_graph(data_file_path)

    # Set the budget and other parameters
    budget = 10
    method = 'AA'
    num_iterations = 100

    # Run budgeted influence maximization
    seed_set = BIM(G, budget, method, num_iterations)
    print("Seed set:", seed_set)


if __name__ == "__main__":
    main()
