#Function to create the F1, PC and PQ plot to evaluate the performance of LSH. 

from lsh import *
import matplotlib.pyplot as plt
import numpy as np

def plot_lsh(sig_matrix, true_pairs): 
    num_rows_sig, num_cols_sig = sig_matrix.shape
    total_comparisons = (num_cols_sig*(num_cols_sig-1))/2 
    n = sig_matrix.shape[0]
    D_n = len(true_pairs)

    PQ_values = []
    PC_values = []
    fraction_of_comparisons_values = []

    for b in range(1, n): 
        if n % b != 0:  # Check if n is divisible by b
            continue  # Skip this b if n is not divisible by b

        r = n // b  # Use integer division to determine r
        
        candidate_pairs = lsh(sig_matrix, b, r)

        N_c = len(candidate_pairs)
        D_f = len(candidate_pairs.intersection(true_pairs))

        PQ = D_f / N_c
        PC = D_f / D_n
        F_1 = (2 * (PQ * PC)) / (PQ + PC)
        fraction_of_comparisons = N_c / total_comparisons

        PQ_values.append(PQ)
        PC_values.append(PC)
        fraction_of_comparisons_values.append(fraction_of_comparisons)
    
    
    #Plot PC and PQ against the fraction of comparisons. 
    # Convert lists to numpy arrays for plotting
    PQ_values = np.array(PQ_values)
    PC_values = np.array(PC_values)
    fraction_of_comparisons_values = np.array(fraction_of_comparisons_values)

    # Plotting PQ and PC against fraction of comparisons
    plt.figure(figsize=(14, 5))

    # Plotting PQ and PC against fraction of comparisons
    plt.figure(figsize=(14, 5))

    # Pair Quality plot
    plt.subplot(1, 2, 1)
    plt.plot(fraction_of_comparisons_values, PQ_values, label='Pair Quality')
    plt.xlabel('Fraction of Comparisons')
    plt.ylabel('Pair Quality')
    plt.title('Pair Quality vs Fraction of Comparisons')
    plt.legend()

    # Pair Completeness plot
    plt.subplot(1, 2, 2)
    plt.plot(fraction_of_comparisons_values, PC_values, label='Pair Completeness')
    plt.xlabel('Fraction of Comparisons')
    plt.ylabel('Pair Completeness')
    plt.title('Pair Completeness vs Fraction of Comparisons')
    plt.legend()

    plt.tight_layout()
    plt.savefig("LSH.png")
