from itertools import combinations

#Function to extract the candidate pairs using LSH. 
def lsh(sig_matrix, b, r):
    n, num_products = sig_matrix.shape
    assert n == b * r, "Number of rows in signature matrix must equal b * r"
    buckets = {}

    for i in range(b):
        for j in range(num_products):
            # Create hashable tuple key for each column in the band
            key = tuple(sig_matrix[i * r:(i + 1) * r, j])
            buckets.setdefault(key, []).append(j)
    
    candidate_pairs = set()

    for bucket in buckets.values():
        if len(bucket) > 1:
             for i in range(len(bucket)):
                for j in range(i + 1, len(bucket)):
                    pair = (min(bucket[i], bucket[j]), max(bucket[i], bucket[j]))
                    candidate_pairs.add(pair)

    return candidate_pairs
