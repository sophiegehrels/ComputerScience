from msm import aggclustering
from itertools import combinations

#Function to calculate the F1 sores after the MSM algorithm.
def calculate_F1_score(true_pairs, epsilon, distance_matrix):
    clusters = aggclustering(distance_matrix, epsilon)
    cluster_pairs = set()
    for cluster_label in set(clusters):
        product_indices = [i for i, x in enumerate(clusters) if x == cluster_label]
        if len(product_indices) > 1:
            for pair in combinations(product_indices, 2):
                cluster_pairs.add(tuple(sorted(pair)))

    normalized_true_pairs = {tuple(sorted(pair)) for pair in true_pairs}

    # Calculate TP, FP, and FN using the normalized pairs
    TP = len(cluster_pairs.intersection(normalized_true_pairs))
    print(f"TP: {TP}")
    FP = len(cluster_pairs - normalized_true_pairs)
    print(f"FP: {FP}")
    FN = len(normalized_true_pairs - cluster_pairs)
    print(f"FN: {FN}")

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0

    F_1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    print(f"F1: {F_1}")
    return F_1