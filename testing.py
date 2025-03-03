from header import read_data, VALID_REGION_NAMES, VALID_COUNCIL_AREAS
from pprint import pprint  # Only used for test purpose
from datetime import datetime
import csv

'''
def read_data(filename):
    """
    Take a filename and output a dictionary of dictionaries of
    the real estate data contained in that file.
    """
    data = {}
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ID = row["ID"]
            del row["ID"]
            data[ID] = dict(row)

    return data
'''

noisy_data = {}
with open('sales_data_noisy_sample.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        ID = row['ID']
        del row['ID']
        noisy_data[ID] = dict(row)

pprint(noisy_data)



# noisy_data = read_data('sales_data_noisy_sample.csv')
# pprint(noisy_data)