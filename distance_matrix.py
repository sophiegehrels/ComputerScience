import numpy as np
from msm import *

#Function to generate the distance matrix
def generate_distance_matrix_opt(full_product_list, all_pairs, gamma, alpha, beta, mu, delta, epsilon_TMWM):
    n = len(full_product_list)
    large_number = 1e12
    dist = np.full((n, n), large_number)
    count_pairs = 0

    # Preprocessing step
    precomputed_data = {
        i: {
            'brand': get_brand_or_brand_name(pi['featuresMap']),
            'shop': pi['shop'],
            'title': pi['title'],
            'featuresMap': pi['featuresMap'],
            'featuresKeys': set(pi['featuresMap'].keys())
        } for i, pi in enumerate(full_product_list)
    }
    
    for pi_x, pj_y in all_pairs: 
        count_pairs = count_pairs + 1
        if count_pairs % 5000 == 0: 
            print(count_pairs)
        data_i = precomputed_data[pi_x]
        data_j = precomputed_data[pj_y]

        if data_i['shop'] == data_j['shop'] or (data_i['brand'] != data_j['brand'] and data_i['brand'] is not None and data_j['brand'] is not None):
            continue
            
        else: 
            sim = 0
            avgSim = 0
            m = 0 
            w = 0
            
            keys_i = data_i['featuresKeys']
            keys_j = data_j['featuresKeys']

            nmk_i_keys = keys_i - keys_j
            nmk_j_keys = keys_j - keys_i

            nmk_i = {k: data_i['featuresMap'][k] for k in nmk_i_keys}
            nmk_j = {k: data_j['featuresMap'][k] for k in nmk_j_keys}

            keys_to_remove_i = set()
            keys_to_remove_j = set()

            for key_i, val_i in data_i['featuresMap'].items():
                for key_j, val_j in data_j['featuresMap'].items():
                    keySim = calcSim(key_i, key_j)
                    if keySim > gamma: 
                        valueSim = calcSim(val_i, val_j)
                        weight = keySim
                        sim = sim + weight * valueSim
                        m = m + 1
                        w = w + weight
                        
                        keys_to_remove_i.add(key_i)
                        keys_to_remove_j.add(key_j)
            
            nmk_i = {k: v for k, v in nmk_i.items() if k not in keys_to_remove_i}
            nmk_j = {k: v for k, v in nmk_j.items() if k not in keys_to_remove_j}
            
            if w > 0:
                avgSim = sim / w
            
            mwPerc = mw(exMW(nmk_i), exMW(nmk_j))
            titleSim = TMWMSim(data_i['title'], data_j['title'], alpha, beta, delta, epsilon_TMWM)

            if titleSim == -1:
                minFeatures = min(len(data_i['featuresKeys']), len(data_j['featuresKeys']))
                theta1 = m/minFeatures
                theta2 = 1-theta1
                hSim = theta1 * avgSim + theta2 * mwPerc
            else: 
                theta1 = (1-mu)*(m / min(len(data_i['featuresKeys']), len(data_j['featuresKeys'])))
                theta2 = 1 - mu - theta1
                hSim = theta1 * avgSim + theta2 * mwPerc + mu * titleSim
            
            dist[pi_x][pj_y] = 1-hSim
    
    # np.save('distance_matrix.npy', dist)
    return dist


def generate_distance_matrix_candidates(full_distance_matrix, candidate_pairs): 
    n = full_distance_matrix.shape[0]
    large_number = 1e12
    dist = np.full((n, n), large_number)

     # Convert the list of pairs into two arrays: rows and cols
    rows, cols = zip(*candidate_pairs)
    # Update the matrix in a vectorized manner
    dist[rows, cols] = full_distance_matrix[rows, cols]
    return dist


