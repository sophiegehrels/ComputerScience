import json 
import re
import copy

import re

def clean_data(value):
    # Convert to lower case first
    value = value.lower()

    # Normalize variations of "inch", "hertz", "lbs", "mw", and "wifi" 
    inch_variations = [r'["”]', r'inch', r'inches', r'-inch', r' inch']
    for var in inch_variations:
        value = re.sub(var, 'inch', value)

    hertz_variations = [r'hz', r'hertz', r'-hz', r' hz']
    for var in hertz_variations:
        value = re.sub(var, 'hz', value)

    pounds_variations = [r'pounds', r' pounds', r'lb', r' lbs', r'lbs.']
    for var in pounds_variations:
        value = re.sub(var, 'lbs', value)
    
    mw_variations = [r' mw', r'mw']
    for var in mw_variations:
        value = re.sub(var, 'mw', value)

    wifi_variations = [r'wifi', r'wi-fi', r'wifi ready', r'wifi built-in', r'built-in wifi', r'wi-fi built-in']
    for var in wifi_variations:
       value = re.sub(var, 'wifi', value)
    
    # Function to remove non-alphanumeric tokens and spaces before units
    def clean_unit(match):
        unit = match.group(0)
        return re.sub(r'^[\s\W]+', '', unit)

    # Apply the cleaning function to each instance of "inch" or "hz"
    value = re.sub(r'[\s\W]*(inch|hz)\b', clean_unit, value)

    return value

def clean_tv_data(file_path, output_file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Create a deep copy of the original data
    data_cleaned = copy.deepcopy(data)

    for model_id, list_tvs in data_cleaned.items():
        for tv in list_tvs:
            if 'featuresMap' in tv:
                for feature, v in tv['featuresMap'].items():
                    cleaned_val = clean_data(v)
                    tv['featuresMap'][feature] = cleaned_val
            if 'title' in tv:
                tv['title'] = clean_data(tv['title'])

    # Save the cleaned data to a new JSON file
    with open(output_file_path, 'w') as file:
        json.dump(data_cleaned, file, indent=4)

input_file_path = "TVs-all-merged.json"
output_file_path = "TVs-all-merged-cleaned.json"
clean_tv_data(input_file_path, output_file_path)

