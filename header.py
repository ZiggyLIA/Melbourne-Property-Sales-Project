import csv

VALID_REGION_NAMES = ["Eastern Metropolitan", "Northern Metropolitan", "South-Eastern Metropolitan",
                      "Southern Metropolitan", "Western Metropolitan"]

VALID_COUNCIL_AREAS = ["Banyule", "Brimbank", "Darebin", "Hume", "Knox", "Maribyrnong", "Melbourne", "Moonee Valley",
                       "Moreland", "Whittlesea", "Yarra"]


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