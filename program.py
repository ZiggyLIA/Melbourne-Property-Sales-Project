from header import read_data, VALID_REGION_NAMES, VALID_COUNCIL_AREAS
from pprint import pprint  # Only used for test purpose
from datetime import datetime
from header import read_data
from datetime import datetime
import statistics
import csv

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



# This function is to enter the dataset, sale agent name and year.
# It will return the maximum, minimum, median, and sum of the property sales of the agent for this year.
def seller_sale_stats(data, seller, year):
    # Set up the structure of the final result
    sale_data = {'seller': seller,
                 'stats': {'max': 0,
                           'med': 0,
                           'min': 0,
                           'sum': 0}}
    # Convert the 'SaleDate' format into year only
    date_format = "%d/%m/%Y"
    for key in data:
        formalized_date = datetime.strptime(data[key]['SaleDate'], date_format)
        data[key]['SaleDate'] = formalized_date.year # replace the dd/mm/yyyy to yyyy

    agent_selling_data = []
    current_suburb = None
    price = 0
    for key, value in data.items():
        if value['Seller'] == seller and value['SaleDate'] == int(year):
            price = int(value['Price'])
            agent_selling_data.append(int(price))
            current_suburb = value['Suburb']
            # Filter out the maximum and minimum prices and \
            # the corresponding suburbs
            if sale_data['stats']['max'] == 0 or price >= sale_data['stats']['max'][0]:
                sale_data['stats']['max'] = (price, current_suburb)
            if sale_data['stats']['min'] == 0 or price <= sale_data['stats']['min'][0]:
                sale_data['stats']['min'] = (price, current_suburb)
            else:
                continue
    # Compute the median and sum of the prices and add to the sale_data
    if len(agent_selling_data) != 0:
        sale_data['stats']['sum'] = sum(agent_selling_data)
        if type(statistics.median(agent_selling_data)) == float:
            sale_data['stats']['med'] = round(statistics.median(agent_selling_data))
        if type(statistics.median(agent_selling_data)) == int:
            sale_data['stats']['med'] = statistics.median(agent_selling_data)

    return sale_data


# Define a function to compute the similarity degree between\
# the selected data and the data from the interested suburb
def similarity_distance(value1, value2):
    bedrooms_si = int(value1['Bedrooms']) - int(value2['Bedrooms'])
    bathrooms_si = int(value1['Bathrooms']) - int(value2['Bathrooms'])
    carspace_si = int(value1['CarSpaces']) - int(value2['CarSpaces'])
    if int(value1['Landsize']) >= int(value2['Landsize']):
        land_si = int(value1['Landsize']) / int(value2['Landsize'])
    else:
        land_si = int(value2['Landsize']) / int(value1['Landsize'])
    score = abs(bedrooms_si) + abs(bathrooms_si) + abs(carspace_si) + land_si
    return round(score,2)


# This function is to search through the data input to retrieve the property in suburb that is most similar to the \
# property associated with sale_id, and get the sale price of that property.
def price_comparison(input_sale_id, data, suburb):
    # Check if the input_sale_id exist in the data
    if input_sale_id not in data.keys():
        return 'There is no sales record with the input ID provided'
    # Collect the data that match the input suburb
    # If the key is same as the input_sale_id, then skip and move \
    # to next loop to avoid self comparison
    dataOf_match_suburb = [value for key, value in data.items()
                           if key != input_sale_id and value['Suburb']==suburb]
    # Check if there is no match suburb data
    if len(dataOf_match_suburb) == 0:
        return 'There are no sales records in the comparison suburb provided'
    # Find the minimum value of the property similarity
    min_si = 100
    corresponding_price = []
    for match_data in dataOf_match_suburb:
        si_score = similarity_distance(data[input_sale_id], match_data)
        # print(si_score)
        if si_score < min_si or si_score is None:
            min_si = si_score
            corresponding_price = int(match_data['Price'])
            # print(f"p:{corresponding_price}")
        elif si_score == min_si:
            corresponding_price = [corresponding_price]
            corresponding_price.append(int(match_data['Price']))
        else:
            continue
    # If data type of corresponding_price is int, which mean it has one result
    if type(corresponding_price) == int:
        return (f"The input property at {data[input_sale_id]['Address']} in the suburb of "
                f"{data[input_sale_id]['Suburb']} has a sale price of "
                f"{data[input_sale_id]['Price']}\nThe most similar "
                f"property in the suburb of {suburb} sold for {corresponding_price}")
    # Compute the average price if there are more than 1 same score data
    if len(corresponding_price) > 1:
        corresponding_price = sum(corresponding_price) / len(corresponding_price)
        if corresponding_price % 2 == 0:
            return (f"The input property at {data[input_sale_id]['Address']} in the suburb of "
                    f"{data[input_sale_id]['Suburb']} has a sale price of "
                    f"{data[input_sale_id]['Price']}\nThe most similar "
                    f"properties in the suburb of {suburb} sold for an average price of {int(corresponding_price)}")
        # If the average price is a float, round the result to 2 decimal places
        else:
            return (f"The input property at {data[input_sale_id]['Address']} in the suburb of "
                f"{data[input_sale_id]['Suburb']} has a sale price of "
                f"{data[input_sale_id]['Price']}\nThe most similar "
                f"properties in the suburb of {suburb} sold for an average price of {round(corresponding_price,2)}")


# to test your function with 'noisy_data.csv' or another CSV file,
# change the value of this variable
test_file = 'sales_data_noisy_sample.csv'
data_noisy = read_data('sales_data_noisy_sample.csv')

# you don't need to modify the code below
if __name__ == '__main__':
    data_noisy = read_data(test_file)
    data_cleaned = sales_data_clean(data_noisy)
    pprint(data_cleaned)