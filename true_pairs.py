#Find the true duplicate pairs, necessary the computet the evaluation metrics. 

from collections import defaultdict
from itertools import combinations

def find_set_duplicates(list_products):
    # Dictionary to hold the products grouped by their modelID
    true_duplicates = defaultdict(list)

    # Loop through all products and group them by modelID
    for idx, product in enumerate(list_products):
        true_duplicates[product['modelID']].append(idx)

    # Generate true_pairs directly from the true_duplicates
    true_pairs = set()
    for indices in true_duplicates.values():
        if len(indices) > 1:
            for pair in combinations(indices, 2):
                true_pairs.add(tuple(sorted(pair)))

    return true_pairs

def find_set_duplicates_subset(list_products, original_indices):
    # Dictionary to hold the products grouped by their modelID
    true_duplicates = defaultdict(list)

    # Loop through all products and their original indices, group them by modelID
    for original_idx, product in zip(original_indices, list_products):
        true_duplicates[product['modelID']].append(original_idx)

    # Generate true_pairs using the original indices
    true_pairs = set()
    for indices in true_duplicates.values():
        if len(indices) > 1:
            for pair in combinations(indices, 2):
                true_pairs.add(tuple(sorted(pair)))

    return true_pairs