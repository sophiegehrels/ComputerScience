# ComputerScience
This project implements an extension of the MSMP+ (cited below) duplicate detection method with a more thorough data cleaning procedure, and an extension of the model word definition. 

MSMP+:
Hartveld, A., van Keulen, M., Mathol, D., van Noort, T., Plaatsman, T., Frasincar, F., & Schouten, K. (2018, May). An LSH-based model-words-driven product duplicate detection method. In International Conference on Advanced Information Systems Engineering (pp. 409-423). Cham: Springer International Publishing.

# Set-Up
- Set-up the virtual environment using Python 3.11
- Open new environment
- Make sure you save the TVs-all-merged.json data in the same folder containing al the code. 
- Navigate to the main file.
- Install the required packages.
- Open the code and edit (We used Visual Studio Code), you can run the main file to run the entire bootstrap. 
- To retrieve the plots to evaluate the bootstrap (F1), run the bootstrapping.ipynb file.
- To retrieve the plots after the LSH, run the lsh_plotting.ipynb file. 

# What is included
- TVs-all-merged.json: contains the raw television data. 
- TVs-all-merged_old.json: contains cleaned data with the old approach. 
- TVs-all-merged_imrpoved.json: contains cleaned data with the improved approach. 
- Main.py: Module that runs the final code with the bootstrap, including all necessary functions. 
- binary_vectors.py: function to create a binary vector with the old approach. 
- binary_vectors_improved.py: function to create a binary vector with the improved approach, adding brand names to the title model words.
- data_cleaning.py: module to clean the data using the old approach. 
- data_cleaning_improved.py: module to clean the data using the new approach, including the extra data cleaning steps. 
- bootstrapping.ipynb: Interactive Python Notebook to create the F1 plot after the performed bootstrap. The first cell runs the algorithm with the old approach, the second cell runs the algorithm with the new approach, and the third cell creates the plots. 
- distance_matrix: module to create the distance matrx where all the dissimilarities are stored. 
- f1_scores: module to calculate f1 scores. 
- lsh: module that includes computation of LSH. 
- lsh_plotting.ipynb: Interactive Python Notebook to create the PC, PQ, and F1 plot after the performed LSH. The first cell runs the algorithm with the old approach, the second cell runs the algorithm with the new approach, and the third cell creates the plots. 
- minhashing.py: module to create the signature matrix. 
- true_pairs.py: module to find the true duplicates in a list of products. 
- utilities: module that combines several functions (binary vector, minhash, and true duplicates) to retrieve all possible pairs, the true pairs, and the signature_matrix. This function is called in the bootstrap to compute the evaluation metrics. 

# How to run
- Run the main method in the main.py module
- Note that the running times may be long
