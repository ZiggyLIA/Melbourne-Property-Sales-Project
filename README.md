# For this project you will be dealing with a dataset of house/property sales in metropolitan Melbourne during the years 2016 and 2017.

## This project will filter out the incorrect information from the given dataset and either remove it or replace it with the correct data.

CSV is a simple file format which is widely used for storing tabular data (data that consists of columns and rows). 
In CSV, columns are separated by commas, and rows are separated by newlines (so every line of the text file corresponds to a row of the data).

### The sales data in this project contains the following columns:
* ID: Row record ID.
* Suburb: The suburb where the property is located.
* Address: The property address.
* Postcode: The property postcode, a 4-digit number.
* CouncilArea: The municipality or council area under which the property falls.
* Regionname: The region of metropolitan Melbourne under which the property falls.
* Price: How much the property sold for. This value is a whole number.
* SaleDate: The date of property sale, in the dd/mm/yyyy format.
* Seller: The real estate agency that sold the property.
* Bedrooms: Number of bedrooms.
* Bathrooms: Number of bathrooms.
* CarSpaces: Number of car spaces.
* Landsize: NSize of the land. This value is a whole number.
* Latitude: The latitude geolocation coordinate of the property
* Longitude: The longitude geolocation coordinate of the property


### Quick explanation of these files is in order:
* program.py: main program
* header.py: A file containing some useful functions and constants. We have already imported the relevant functions and constants for you in each question.
* sales_data_noisy_sample.csv & sales_data_noisy_sample2.csv: These are the real estate sales data files provided to you, and you can use them to test your functions as you work through the questions. 

### Requirements (Part 1):
You have been provided with CSV files containing data about real estate sales in Melbourne. Unfortunately, the data is 'noisy': some people have made data entry mistakes, or intentionally entered incorrect data. 
Your first task is to clean up the noisy data for later analysis.

#### There are a few particular errors in this data:
* Typos have occurred in the Price column, resulting in some values that are not numeric whole numbers.
* People have entered Regionname values that are no longer current, valid region names. The valid regions are listed in a list called VALID_REGION_NAMES, which is given to you.
* Some people have formatted the sale date incorrectly, such that it is either not of the form dd/mm/yyyy (variations d/mm/yyyy, dd/m/yyyy and d/m/yyyy would also be valid) or contains invalid dates, 
such as 31/11/2016. If a date does not fall under the year 2016 or the year 2017, it is also considered invalid.
* Some Postcode values are not valid Melbourne postcode values: they need to be 4-digit integers that start with 3.
* This data has been read directly from a CSV file, and is noisy. Your function should construct and return a new data dictionary which is identical to the input dictionary, except that invalid data, as described by the rules above, have been replaced with None. In doing so, **your program should aim to not modify the input argument dictionary**, **data**. 
* There is also one further type of potential error in the noisy data that needs to be fixed. Valid values in the **CouncilArea** column must be in the set of Melbourne council areas: Banyule, Brimbank, Darebin, Hume, Knox, Maribyrnong, Melbourne, Moonee Valley, Moreland, Whittlesea and Yarra. This list of valid councils can be found in the list **VALID_COUNCIL_AREAS**, which is given to you.
* However, values in the **CouncilArea** column could be incorrectly spelt or contain extra characters. Examples of such incorrect values are: Morelnd; Yara; nox; aDarebin; Melbun; Honey Valley.
* Your program should attempt to replace incorrect values with their correct council area value by using the following set similarity measure, which we use to provide a number representing the similarity between two strings. Suppose we have the following two example strings:
  * string1 = "Aaa bBb ccC" # The set representation of string1 is {'a', 'b', 'c', ' '}
  * string2 = "bbb ccc ddd" # The set representation of string2 is {'b', 'c', 'd', ' '}
  * Notice that for our purposes/definition case does not matter (e.g. 'A' is the same as 'a') and that space is also a character.
  * The set similarity (**Sim**) measure for **string1** and **string2** is given by the formula:
    * Sim(string1, string2) = |S1 ∩ S2| / |S1 ∪ S2| (Where ∩ is set intersection, ∪ is set union, and |X| is the length of set X)
    * Sim(string1, string2) = |{a, b, c, (space)} ∩ {b, c, d, (space)}| / |{a, b, c, (space)} ∪ {b, c, d, (space)}| = |{b, c, (space)}| / |{a, b, c, d, (space)}| = 3/5 = 0.6
  * when your program comes across an incorrect council area value it should compare that incorrect value with all of the correct council area strings using the Sim function, and then replace the incorrect string with the valid council area value that it has the highest Sim measure with. For example, when the incorrect value is "Melbun", the measure comparisons are:
    * Sim("Banyule", "Melbun") = 0.625
    * Sim("Brimbank", "Melbun")  = 0.3
    * Sim("Darebin", "Melbun") = 0.3
    * Sim("Hume", "Melbun")  = 0.42857142857142855
    * Sim("Knox", "Melbun") = 0.1111111111111111
    * Sim("Maribyrnong", "Melbun") = 0.25
    * Sim("Melbourne", "Melbun")  = 0.75
    * Sim("Moonee Valley", "Melbun")  = 0.36363636363636365
    * Sim("Moreland", "Melbun")  = 0.4
    * Sim("Whittlesea", "Melbun")  = 0.16666666666666666
    * Sim("Yarra", "Melbun")  = 0.0
    * Since Sim("Melbourne", "Melbun") is the highest of all these values, the incorrect "Melbun" would be replaced by "Melbourne".
  * when the incorrect council area string value is "Meorln", the two highest similarities with correct council area values are:
    * Sim("Moreland", "Meorln") = Sim("Melbourne", "Meorln") = 0.75
    * Since the program has no further way of deciding between the two, it just replaces "Meorln" with None.

#### Example
### The first example applies the sales_data_clean function to the input data contained in sales_data_noisy_sample.csv. Notice the use of Python's pprint function in this example, which is like print but 'beautifies' the output, so it is easier to read. This is particularly useful to visualise dictionaries.
```python
>>> data_noisy = read_data('sales_data_noisy_sample.csv')
>>> pprint(sales_data_clean(data_noisy))

> {'1': {'Address': '8 Watchtower Rd',
       'Bathrooms': '1',
       'Bedrooms': '3',
       'CarSpaces': '2',
       'CouncilArea': 'Moreland',
       'Landsize': '142',
       'Latitude': '-37.7382',
       'Longitude': '144.973',
       'Postcode': '3058',
       'Price': '675000',
       'Regionname': 'Northern Metropolitan',
       'SaleDate': '4/02/2016',
       'Seller': 'Walshe',
       'Suburb': 'Coburg'},
 '2': {'Address': '25 Bloomburg St',
       'Bathrooms': '1',
       'Bedrooms': '2',
       'CarSpaces': '0',
       'CouncilArea': 'Yarra',
       'Landsize': '156',
       'Latitude': '-37.8079',
       'Longitude': '144.9934',
       'Postcode': None,
       'Price': '1035000',
       'Regionname': None,
       'SaleDate': None,
       'Seller': 'Biggin',
       'Suburb': 'Abbotsford'},
 '3': {'Address': '234 Coppin St',
       'Bathrooms': '2',
       'Bedrooms': '3',
       'CarSpaces': '0',
       'CouncilArea': 'Yarra',
       'Landsize': '194',
       'Latitude': '-37.8265',
       'Longitude': '145.0022',
       'Postcode': '3121',
       'Price': '1102000',
       'Regionname': 'Northern Metropolitan',
       'SaleDate': '4/02/2016',
       'Seller': 'Dingle',
       'Suburb': 'Richmond'},
 '4': {'Address': '11/1051 Pascoe Vale Rd',
       'Bathrooms': '1',
       'Bedrooms': '2',
       'CarSpaces': '1',
       'CouncilArea': 'Hume',
       'Landsize': '197',
       'Latitude': '-37.6859',
       'Longitude': '144.9164',
       'Postcode': '3047',
       'Price': None,
       'Regionname': 'Northern Metropolitan',
       'SaleDate': '16/04/2016',
       'Seller': 'Raine',
       'Suburb': 'Jacana'},
 '5': {'Address': '4 Myrtle Gr',
       'Bathrooms': '1',
       'Bedrooms': '3',
       'CarSpaces': '2',
       'CouncilArea': 'Moonee Valley',
       'Landsize': '573',
       'Latitude': '-37.72908',
       'Longitude': '144.88327',
       'Postcode': '3042',
       'Price': '905000',
       'Regionname': None,
       'SaleDate': '24/06/2017',
       'Seller': 'Jellis',
       'Suburb': 'Airport West'},
 '6': {'Address': '1/6 Patmore Ct',
       'Bathrooms': '1',
       'Bedrooms': '2',
       'CarSpaces': '1',
       'CouncilArea': 'Whittlesea',
       'Landsize': '257',
       'Latitude': '-37.65636',
       'Longitude': '145.03997',
       'Postcode': '3082',
       'Price': '421000',
       'Regionname': 'Northern Metropolitan',
       'SaleDate': None,
       'Seller': 'Ray',
       'Suburb': 'Mill Park'},
 '7': {'Address': '2/4 Currajong St',
       'Bathrooms': '1',
       'Bedrooms': '3',
       'CarSpaces': '1',
       'CouncilArea': 'Whittlesea',
       'Landsize': '340',
       'Latitude': '-37.67803',
       'Longitude': '145.01769',
       'Postcode': '3074',
       'Price': None,
       'Regionname': None,
       'SaleDate': '24/06/2017',
       'Seller': 'Love',
       'Suburb': 'Thomastown'},
 '8': {'Address': '10/30 Pickett St',
       'Bathrooms': '1',
       'Bedrooms': '1',
       'CarSpaces': '0',
       'CouncilArea': 'Maribyrnong',
       'Landsize': '30',
       'Latitude': '-37.80141',
       'Longitude': '144.89587',
       'Postcode': None,
       'Price': '170000',
       'Regionname': 'Western Metropolitan',
       'SaleDate': '1/07/2017',
       'Seller': 'Burnham',
       'Suburb': 'Footscray'}}
```

### Requirements (Part 2):
Write a function called seller_sale_stats(data, seller, year) which takes three arguments: a dictionary of clean data in the format returned by read_data, the name of a seller (i.e. real estate agency), and a year (yyyy).

For the given seller and the given year, calculate the following sales stats:
* **median** sale Price, rounded to the nearest whole number. The median is the middle number in a sorted list of numbers. For example, the median of [1, 2, 3, 4, 5] is 3. If there is an even number of numbers, then the median is calculated by adding the two middle numbers and dividing by 2. For example, the median of [1, 2, 3, 4, 5, 6] is (3+4)/2 = 3.5
* **sum total** Price
* **minimum** instance of Price. This should be presented as a tuple consisting of the price and the suburb with the minimum price. For example, (675000, Coburg). If more than one suburb has the minimum price, just return whichever suburb appears last in the CSV file.
* **maximum** instance of Price. This should be presented as a tuple consisting of the price and the suburb with the maximum price. For example, (1000000, Brunswick). If more than one suburb has the maximum price, just return whichever suburb appears last in the CSV file.

The result is a dictionary with this information, as shown in the examples below. If a seller does not have any sales information for the year, then the values are set to 0.

#### Example 1:
```python
>>> data_cleaned = read_data("sales_data_clean.csv")
>>> pprint(seller_sale_stats(data_cleaned, 'Love', '2017'))

> {'seller': 'Love',
 'stats': {'max': (935000, 'Reservoir'),
           'med': 590250,
           'min': (401500, 'Epping'),
           'sum': 13658500}}
```

#### Example 2:
```python
>>> data_cleaned = read_data("sales_data_clean.csv")
>>> pprint(seller_sale_stats(data_cleaned, 'Nelson', '2016'))

> {'seller': 'Nelson',
 'stats': {'max': (4011000, 'Fitzroy'),
           'med': 1133000,
           'min': (400000, 'Brunswick West'),
           'sum': 180134000}}
```

#### Example 3:
In the example 3, there is no data for the given seller and year, so the results returned are all 0.
```python
>>> data_cleaned = read_data("sales_data_clean.csv")
>>> pprint(seller_sale_stats(data_cleaned, 'Nelson', '2015'))

> {'seller': 'Nelson', 'stats': {'max': 0, 'med': 0, 'min': 0, 'sum': 0}}
```
### Requirements (Part 3):
The similarity distance between two properties is defined by the fields of Bedrooms, Bathrooms, CarSpaces and Landsize. Start with a similarity_distance score of 0, and proceed as follows:
* add the difference in number of bedrooms between the two properties to the similarity_distance score
* add the difference in number of bathrooms between the two properties to the similarity_distance score
* add the difference in number of car spaces between the two properties to the similarity_distance score
* for land size, select the smaller of the two land sizes and divide that number into the larger landsize. Add the result (rounded to 2 decimal place) to the similarity_distance score.
* **The lower a similarity_distance score, the more similar two properties are** (if two properties have exactly the same values for all of these four fields, then similarity_distance = 1). So, for example, take the following three sales:

| ID |  Suburb | Address  | Bedrooms | Bathrooms | CarSpaces |
|----|---|---|----------|-----------|-----------|
| 1  | Coburg  |  8 Watchtower Rd  | 3        | 1         | 2         |
| 2  | Abbotsford  |  25 Bloomburg St | 2        | 1         | 0         |
| 3  |  Jacana |  11/1051 Pascoe Vale Rd | 2        | 1         | 1         |

The similarity_distance score between sale records 1 and 2 is: (3 - 2) + (1 - 1) + (2 - 0) + (156/142) = 1 + 0 + 2 + 1.1 = 4.1

The similarity_distance score between sale records 1 and 4 is: (3 - 2) + (1 - 1) + (2 - 1) + (197/142) = 1 + 0 + 1 + 1.39 = 3.39

Therefore, by this definition, the properties of records 1 and 4 are more similar than the properties of records 1 and 2.

For this question you are to write a function **price_comparison(sale_id, date, suburb)**, where:
* **sale_id** is the ID of a sale record to be compared against
*  **data** is a dictionary of clean data in the format returned by read_data
* **suburb** is the name of a suburb from which we are finding comparison sales

The objective of **price_comparison()** is to search through the data input to retrieve the property in suburb that is most similar to the property associated with **sale_id**, and get the sale price of that property. If there is more than one such most similar property, obtain the average sale price of them (rounded to the closest integer). 
Once this (possibly average) sale price is determined, the function will return a string message in the form of the examples below.

#### Example 1:
```python
>>> data_cleaned = read_data("sales_data_clean.csv")
>>> print(price_comparison("1", data_cleaned, "Heidelberg"))

The input property at 7/459 Waterdale Rd in the suburb of Heidelberg West has a sale price of 463000
The most similar property in the suburb of Heidelberg sold for 738000
```

#### Example 2:
```python
>>> data_cleaned = read_data("sales_data_clean.csv")
>>> print(price_comparison("621", data_cleaned, "Epping"))

The input property at 48 Fitzgerald Rd in the suburb of Essendon has a sale price of 900000
The most similar property in the suburb of Epping sold for 392250
```

#### Example 3:
```python
>>> data_cleaned = read_data("sales_data_clean.csv")
>>> print(price_comparison("149", data_cleaned, "Brunswick"))

The input property at 25 Brisbane St in the suburb of Albion has a sale price of 463000
The most similar properties in the suburb of Brunswick sold for an average price of 82750
```

#### If:

1: If the given input **sale_id** does not correspond to a sales record:
* Then return the following string message: "There is no sales record with the input ID provided".

2: If the input comparison **suburb** has no sales records to compare against:
* Then return the following string message: "There are no sales records in the comparison suburb provided".

Unless otherwise specified, when dealing with float results throughout your code, round to 2 decimal places.