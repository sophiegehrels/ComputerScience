#Function to perform the MSM algorithm. 

import textdistance
import re
import numpy as np
from strsimpy.qgram import QGram
from binary_vectors_improved import get_model_words_titles, get_unique_model_words_features
from sklearn.cluster import AgglomerativeClustering


def calcCosineSim(a, b):
    set_a = set(a.split())
    set_b = set(b.split())
    
    # Calculate the intersection of the sets
    intersection = set_a.intersection(set_b)
    # Apply the formula |a ∩ b| / (√|a| * √|b|)
    nameCosineSim = len(intersection) / (len(set_a) ** 0.5 * len(set_b) ** 0.5)
    return nameCosineSim 

def split_model_word(model_word):
    non_numeric = re.sub(r'[0-9]', '', model_word)
    numeric = re.sub(r'[^0-9]', '', model_word)
    return non_numeric, numeric

def avgLvSim(set_X, set_Y):
    total_similarity = 0
    total_length = 0
    
    for x in set_X:
        for y in set_Y:
            # Calculate the normalized Levenshtein similarity as 1 - normalized distance
            similarity = 1 - textdistance.levenshtein.normalized_distance(x, y)
            # Weight the similarity by the sum of lengths of x and y
            weight = len(x) + len(y)
            total_similarity += similarity * weight
            total_length += weight

    # The overall average is the total weighted similarity divided by the total length
    return total_similarity / total_length if total_length else 0

def avgLvSimMW(X, Y): 
    similarity_sum = 0
    denominator = 0
    for x in X:
        non_numeric_x, numeric_x = split_model_word(x)
        for y in Y:
            non_numeric_y, numeric_y = split_model_word(y)
            if textdistance.levenshtein.normalized_similarity(non_numeric_x, non_numeric_y) > 0.7 and numeric_x == numeric_y:
                similarity = (1 - textdistance.levenshtein.normalized_distance(x, y)) * (len(x) + len(y))
                similarity_sum += similarity
                denominator += len(x) + len(y)
            
    avg_similarity = similarity_sum / denominator if denominator != 0 else 0

    return avg_similarity

def TMWMSim(p1, p2, alpha, beta, delta, epsilon): 
    # p1, p2 is title (str)
    nameCosineSim = calcCosineSim(p1, p2)
    if nameCosineSim > alpha:
        return 1
    
    modelWordsA = set(get_model_words_titles(p1))
    modelWordsB = set(get_model_words_titles(p2))

    for wordA in modelWordsA: 
        for wordB in modelWordsB: 
            non_numericA, numericA = split_model_word(wordA)
            non_numericB, numericB = split_model_word(wordB)
            if numericA != numericB and textdistance.levenshtein.normalized_similarity(non_numericA, non_numericB) > 0.5:
                return -1
     
    finalNameSim = beta * nameCosineSim + (1 - beta) * avgLvSim(modelWordsA, modelWordsB)

    similarityCheck = False
    for wordA in modelWordsA: 
        for wordB in modelWordsB: 
            non_numericA, numericA = split_model_word(wordA)
            non_numericB, numericB = split_model_word(wordB)
            if numericA == numericB and textdistance.levenshtein.normalized_similarity(non_numericA, non_numericB) > 0.5:
                similarityCheck = True
    
    if similarityCheck == True:
        modelWordSimVal = avgLvSimMW(modelWordsA, modelWordsB)
        finalNameSim = delta * modelWordSimVal + (1-delta) * finalNameSim
    
    if finalNameSim > epsilon: 
        return finalNameSim
    else:
        return -1
    
def calcSim(string1, string2):
    qgram = QGram(3)
    n1 = len((string1))
    n2 = len((string2))
    valueSim = (n1 + n2 - qgram.distance(string1, string2))/ (n1 + n2)
    return valueSim

def get_brand_or_brand_name(features_map):
    # Try to get 'Brand', if not found, try 'Brand Name'
    return features_map.get('Brand') or features_map.get('Brand Name')

def mw(C, D):
    intersection = len(set(C) & set(D))
    union = len(set(C) | set(D))

    return (intersection / union) if union else 0

def exMW(p):
    return set(get_unique_model_words_features([v for v in p.values()]))

def aggclustering(dist_matrix, threshold):
    clustering = AgglomerativeClustering(
        n_clusters=None, 
        linkage='single', 
        distance_threshold=threshold, 
        affinity='precomputed'
    )
    clusters = clustering.fit_predict(dist_matrix)
    return clusters

def MSM(product_list, pairs, gamma, alpha, beta, mu, delta, epsilon_TMWM, epsilon_clustering):
    n = len(product_list)
    large_number = 1e12
    dist = np.full((n, n), large_number)
    for pi_x, pj_y in pairs: 
        pi = product_list[pi_x]
        pj = product_list[pj_y]
        
        pi_brand = get_brand_or_brand_name(pi['featuresMap'])
        pj_brand = get_brand_or_brand_name(pj['featuresMap'])

        if pi['shop'] == pj['shop'] or (pi_brand != pj_brand and pi_brand is not None and pj_brand is not None):
            continue

        else: 
            sim = 0
            avgSim = 0
            m = 0 
            w = 0
            
            keys_i = set(pi['featuresMap'].keys())
            keys_j = set(pj['featuresMap'].keys())

            nmk_i_keys = keys_i - keys_j
            nmk_j_keys = keys_j - keys_i

            nmk_i = {k: pi['featuresMap'][k] for k in nmk_i_keys}
            nmk_j = {k: pj['featuresMap'][k] for k in nmk_j_keys}


            for key_i, val_i in pi['featuresMap'].items():
                for key_j, val_j in pj['featuresMap'].items():
                    keySim = calcSim(key_i, key_j)
                    if keySim > gamma: 
                        valueSim = calcSim(val_i, val_j)
                        weight = keySim
                        sim = sim + weight * valueSim
                        m = m + 1
                        w = w + weight
                        nmk_i.pop(key_i, None)
                        nmk_j.pop(key_j, None)
            
            if w > 0:
                avgSim = sim / w
            
            mwPerc = mw(exMW(nmk_i), exMW(nmk_j))
            titleSim = TMWMSim(pi['title'], pj['title'], alpha, beta, delta, epsilon_TMWM)

            if titleSim == -1:
                minFeatures = min(len(pi['featuresMap']), len(pj['featuresMap']))
                theta1 = m/minFeatures
                theta2 = 1-theta1
                hSim = theta1 * avgSim + theta2 * mwPerc
            else: 
                theta1 = (1-mu)*(m / min(len(pi['featuresMap']), len(pj['featuresMap'])))
                theta2 = 1 - mu - theta1
                hSim = theta1 * avgSim + theta2 * mwPerc + mu * titleSim
                if pj_y == int(pi_x + 1):
                    print(pi_x, pj_y)
                    print(f"hSim: {hSim}, theta1: {theta1}, avgSim: {avgSim}, theta2: {theta2}, mwPerc: {mwPerc}, titleSim: {titleSim}")
            
            dist[pi_x][pj_y] = 1-hSim
    
    return aggclustering(dist, epsilon_clustering)
            
