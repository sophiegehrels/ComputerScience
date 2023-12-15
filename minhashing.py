#Function to minhash a binary matrix, and create a signature matrix

import numpy as np
import random
import sympy

def minhash(binary_matrix): 
    num_rows, num_cols = binary_matrix.shape

    # Set k to 50% of the number of rows
    # k = num_rows // 2 
    k = 800

    # Find a prime number larger than the number of rows
    p = sympy.nextprime(num_rows)

    random.seed(42)  # For reproducibility
    a_values = np.array([random.randint(1, p) for _ in range(k)])
    b_values = np.array([random.randint(0, p) for _ in range(k)])

    signature_matrix = np.full((k, num_cols), np.iinfo(np.int32).max, dtype=np.int32)

    for r in range(num_rows):
        hf = [0] * k
        for i in range(k): 
            hf[i] = hash_function(a_values[i], b_values[i], r, p)
        for c in range(num_cols): 
            if binary_matrix[r][c] == 1:
                for j in range(len(hf)):
                    signature_matrix[j][c] = int(min(signature_matrix[j][c], hf[j]))

    return signature_matrix

# Function to calculate hash values
def hash_function(a, b, x, p):
    return (a + b * x) % p