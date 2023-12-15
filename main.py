#The main function is used to perform the bootstrap, however, no plots are created by running this funtion. 

from data_cleaning_improved import *
from binary_vectors_improved import * 
from minhashing import *
from lsh import *
from true_pairs import *
from plotting import *
from msm import *
from distance_matrix import *
from f1_scores import *
from utilities import *
import itertools

input_file_path = "TVs-all-merged.json"
output_file_path = "TVs-all-merged-cleaned.json"
clean_tv_data(input_file_path, output_file_path)

with open(output_file_path, 'r') as file: 
    data_cleaned = json.load(file)

all_products = [item for model_id, items in data_cleaned.items() for item in items]
all_pairs = list(itertools.combinations(range(len(all_products)), 2))
all_true_pairs = find_set_duplicates(all_products)

# Parameters
gamma = 0.75 
alpha = 0.6 
beta = 0.3 
mu = 0.6
delta = 0.7
epsilon_TMWM = 0

bootstrap_number = 1
train_ratio = 0.63
epsilon_range = [0.25, 0.35, 0.45]
F1_training_scores = {i: {} for i in range(bootstrap_number)}
F1_testing_scores = {i: {} for i in range(bootstrap_number)}

#generate the distance matrix
full_distance_matrix = generate_distance_matrix_opt(all_products, all_pairs, gamma, alpha, beta, mu, delta, epsilon_TMWM)
full_distance_matrix = np.load("distance_matrix_1312.npy")

#perform the bootstrap
for i in range(bootstrap_number): 
    num_products = len(all_products)
    indices = list(range(num_products))

    subset_size = int(num_products * train_ratio)
    train_subset = random.sample(all_products, subset_size)
    test_subset = [product for product in all_products if product not in train_subset]

    train_num_products_subset = len(train_subset)
    train_subset_indices = list(range(train_num_products_subset))
    train_original_indices = [all_products.index(element) for element in train_subset]
    train_index_mapping = {subset_index: original_index for subset_index, original_index in zip(train_subset_indices, train_original_indices)}
    train_pairs, train_true_pairs, train_signature_matrix, n = get_signature_matrix(train_subset)
    for b in range(1, n+1): #     CHANGE TO N+1
        if n % b != 0:  
            continue  

        r = n // b  
        print(b,r)

        F1_training_scores[i][b] = {epsilon_clustering: 0 for epsilon_clustering in epsilon_range}
        F1_testing_scores[i][b] = {'F1': 0, 'fraction_of_comparisons': 0}

        train_candidate_pairs = lsh(train_signature_matrix, b, r)
        train_candidate_pairs_original = {(train_index_mapping[i], train_index_mapping[j]) for i, j in train_candidate_pairs}
        train_true_pairs_original = {(train_index_mapping[i], train_index_mapping[j]) for i, j in train_true_pairs}

        upper_triangular = np.triu(full_distance_matrix)
        dm_symm = upper_triangular + upper_triangular.T - np.diag(np.diag(upper_triangular))
        train_distance_matrix = generate_distance_matrix_candidates(dm_symm, train_candidate_pairs_original)
                
        for epsilon_clustering in epsilon_range: 
            print(epsilon_clustering)
            F_1 = calculate_F1_score(train_true_pairs_original, epsilon_clustering, train_distance_matrix)
            F1_training_scores[i][b][epsilon_clustering] = F_1

        test_num_products_subset = len(test_subset)
        test_subset_indices = list(range(test_num_products_subset))
        test_original_indices = [all_products.index(element) for element in test_subset]
        test_index_mapping = {subset_index: original_index for subset_index, original_index in zip(test_subset_indices, test_original_indices)}
        test_pairs, test_true_pairs, test_signature_matrix, n = get_signature_matrix(test_subset)
    
        optimal_epsilon_for_ib = max(F1_training_scores[i][b], key=lambda epsilon: F1_training_scores[i][b][epsilon])
        test_candidate_pairs = lsh(test_signature_matrix, b, r)
        test_candidate_pairs_original = {(test_index_mapping[i], test_index_mapping[j]) for i, j in test_candidate_pairs}
        test_true_pairs_original = {(test_index_mapping[i], test_index_mapping[j]) for i, j in test_true_pairs}
        test_distance_matrix = generate_distance_matrix_candidates(dm_symm, test_candidate_pairs_original)
        
        F1_testing_scores[i][b]['F1'] = calculate_F1_score(test_true_pairs_original, optimal_epsilon_for_ib, test_distance_matrix)
        F1_testing_scores[i][b]['fraction_of_comparisons'] = len(test_candidate_pairs_original) / (test_num_products_subset * (test_num_products_subset - 1) / 2)


