import re
import numpy as np

#Extract the model words from the title
def get_model_words_titles(title):
    model_words_title = []
    # Updated regex pattern to match the entire model word as per the new definition
    pattern = r'([a-zA-Z0-9]*(([0-9]+[^0-9, ]+)|([^0-9, ]+[0-9]+))[a-zA-Z0-9]*)'

    regex = re.compile(pattern)
    
    # Find all matches of the model word pattern in the title
    matches = regex.findall(title)
    
    # Extend the model words list with the matches
    for match in matches:
        # Only add the full match, not the subgroups
        model_words_title.append(match[0])

    return model_words_title

#Extract the brand names from the features map
def extract_unique_brand_names(products):
    brand_names = set()  # Using a set to store unique brand names
    for product in products:
        # Extract the brand name using the 'Brand' or 'Brand Name' keys
        brand = product.get('featuresMap', {}).get('Brand') or product.get('featuresMap', {}).get('Brand Name')
        if brand:
            brand_names.add(brand)  # Add to the set, duplicates will be automatically ignored
    return brand_names

#Create a list of unique title model words
def get_unique_model_words(titles_list):
    all_model_words_title = []
    for title in titles_list:
        model_words = get_model_words_titles(title)
        all_model_words_title.extend(model_words)
    return list(set(all_model_words_title))

#Extract model words from the features map
def get_model_words_values(value):
    model_words_keyvalue = []
    # Updated regex pattern to match the model word definition for key-value pairs
    pattern = r'(^\d+(\.\d+)?[a-zA-Z]*$|^\d+(\.\d+)?$)'

    regex = re.compile(pattern)

    # Find all matches of the model word pattern in the value
    matches = regex.findall(value)
    
    # Extend the model words list with the numeric part of the matches
    for match in matches:
        # Extracting the numeric part, removing the alphabetic characters
        numeric_part = re.match(r'^\d+(\.\d+)?', match[0])
        if numeric_part:
            model_words_keyvalue.append(numeric_part.group())

    return model_words_keyvalue

#Create a list of unique feature model words
def get_unique_model_words_features(features_list):
    all_model_words_feature = []
    for feature in features_list:
        model_words = get_model_words_values(feature)
        all_model_words_feature.extend(model_words)
    return list(set(all_model_words_feature))


import numpy as np
#obtain binary vector, with the set of brand names added to the title model words. 
def obtain_binary_matrix(products_subset):
    # Extract titles and features more efficiently
    titles_list = [product['title'] for product in products_subset]
    unique_model_words_title = set(get_unique_model_words(titles_list))
    unique_brand_names = extract_unique_brand_names(products_subset)
    features_values = [value for product in products_subset for value in product.get('featuresMap', {}).values()]
    unique_model_words_features = set(get_unique_model_words_features(features_values))

    all_mw = set(unique_model_words_title.union(unique_model_words_features)).union(unique_brand_names)

    # Initialize the matrix with zeros
    binary_matrix = np.zeros((len(all_mw), len(products_subset)), dtype=int)
    print(f"Length binary matrix is: {len(all_mw)}")
    # Iterate through each product and update the matrix
    for product_index, product in enumerate(products_subset):
        title = product['title']
        features_values = product.get('featuresMap', {}).values()

        for mw_index, mw in enumerate(all_mw):
             if (mw in (set((unique_model_words_title).union(unique_brand_names)) or unique_model_words_features) and mw in features_values) or \
                 (mw in (set((unique_model_words_title).union(unique_brand_names))) and mw in title):
                binary_matrix[mw_index][product_index] = 1
    return binary_matrix

    

