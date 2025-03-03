from header import read_data, VALID_REGION_NAMES, VALID_COUNCIL_AREAS
from pprint import pprint  # Only used for test purpose
from datetime import datetime
import csv

# !!!REMOVE THESE COMMENTS BEFORE SUBMITTING!!!
# Use copy.deepcopy() will lose 50% (1 mark) for approach.

# This function is to measure the set similarity of two input strings
# The return value is the set similarity score
def set_similarity(s1, s2):
    # replace 'pass' with your code
    set1 = set(s1.lower())
    set2 = set(s2.lower())
    rate = len(set1 & set2) / len(set1 | set2)
    return rate


# Convert csv data to dictionary format
def read_data(filename):
    """
    Take a filename and output a dictionary of dictionaries of
    the real estate data contained in that file.
    """
    data = {}
    # reads the CSV file and treats the first row as the header, using it as keys for the dictionary.
    # Each subsequent row is then read as a dictionary where column names serve as keys
    # And the corresponding values from each row become dictionary values.
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ID = row["ID"]
            del row["ID"]
            data[ID] = dict(row)

    return data


# Define aa function to replace invalid region name to None
def clean_regionName(data):
    VALID_REGION_NAMES = ["Eastern Metropolitan", "Northern Metropolitan", "South-Eastern Metropolitan",
                          "Southern Metropolitan", "Western Metropolitan"]
    for key in data:
        if data[key]['Regionname'] not in VALID_REGION_NAMES:
            new_data = data[key]['Regionname'] = None
    return data


# This function is to clean the sales data and replace the incorrect CouncilArea
# The return value is a dict with cleaned data
# THE INPUT DATA (DICT) SHOULD NOT BE MODIFIED
def sales_data_clean(data):
    # replace 'pass' with your code
    # replace 'pass' with your code
    new_dict = {}
    for key, value in data.items():
        new_dict[key]=value.copy()
    # Replace invalid prices to None
    for key in new_dict:
        if not new_dict[key]['Price'].isdigit():
            new_data = new_dict[key]['Price'] = None
    # Replace invalid postcode to None
    for key in new_dict:
        if not new_dict[key]['Postcode'].startswith('3') or not new_dict[key]['Postcode'].isdigit():
            new_data = new_dict[key]['Postcode'] = None
        elif len(new_dict[key]['Postcode']) != 4:
            new_data = new_dict[key]['Postcode'] = None
    # Replace invalid date to None
    date_format = "%d/%m/%Y"
    for key in new_dict:
        # Check which SaleDate doesn't follow the date_format
        try:
            check_date = datetime.strptime(new_dict[key]['SaleDate'], date_format)
        # If the Exception "ValueError" occurs, then replace the current saledate to None
        except ValueError:
            new_dict[key]['SaleDate'] = None
        # Replace the SaleDate that are not 2016 or 2017 to None
        if check_date.year not in [2016, 2017]:
            new_dict[key]['SaleDate'] = None
    # Replace the invalid region name to None
    new_dict = clean_regionName(new_dict)
    # Replace the invalid CouncilArea to Correct one
    VALID_COUNCIL_AREAS = ["Banyule", "Brimbank", "Darebin", "Hume",
                           "Knox", "Maribyrnong",
                           "Melbourne", "Moonee Valley",
                           "Moreland", "Whittlesea", "Yarra"]
    # Extract the list of set that contains each pair of key and value
    key_values = new_dict.items()
    for key, value in key_values:
        original_area = value['CouncilArea']
        max_sim = 0
        top_rate_area = None
        for va in VALID_COUNCIL_AREAS:
            sim_rate = set_similarity(va, original_area)
            if sim_rate > max_sim:
                max_sim = sim_rate
                top_rate_area = va
            elif sim_rate == max_sim:
                top_rate_area = None
        value['CouncilArea'] = top_rate_area

    return new_dict


# to test your function with 'noisy_data.csv' or another CSV file,
# change the value of this variable
test_file = 'sales_data_noisy_sample.csv'
data_noisy = read_data('sales_data_noisy_sample.csv')

# you don't need to modify the code below
if __name__ == '__main__':
    data_noisy = read_data(test_file)
    data_cleaned = sales_data_clean(data_noisy)
    pprint(data_cleaned)