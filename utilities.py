#Utility function that combines several functions (find_set_duplicates, obtain_binary_matrix, minhash) 
#to easily retrieve the signature matrix, true pairs, pairs, and n, by only calling this function. (used in the bootstrap)

import itertools
from data_cleaning import *
from binary_vectors import * 
from minhashing import *
from lsh import *
from true_pairs import *
from msm import *
from distance_matrix import *
from f1_scores import *
from utilities import *


def get_signature_matrix(products):
    pairs = list(itertools.combinations(range(len(products)), 2))
    true_pairs = find_set_duplicates(products)
    binary_matrix = obtain_binary_matrix(products)
    signature_matrix = minhash(binary_matrix)
    rows, cols = signature_matrix.shape
    n = rows

    return pairs, true_pairs, signature_matrix, n