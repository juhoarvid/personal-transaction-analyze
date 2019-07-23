from prettytable import PrettyTable

year = PrettyTable()
year.field_names = ["Category", "Tammi", "Helmi", "Maalis", "Huhti", "Touko",
    "Kesa", "Heina", "Elo", "Syys", "Loka", "Marras", "Joulu", "YHT", "KA"]
#year.add_row(["Ruoka", 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, -12, "paljon", "ka"])

print(year)

import json
import random

with open('nordea_categories.json', 'r') as handle:
    parsed = json.load(handle)
for cat in parsed.keys():
    line = [cat]
    amounts = random.sample(range(-1000,0), 12)
    total = int(sum(amounts))
    average = int(sum(amounts)/len(amounts))
    line.extend(amounts)
    line.append(total)
    line.append(average)
    year.add_row(line)
print(year)

def print_year(year_transactions):
    """
    orderedDict:
    {year : { 
        Jan: {cat1: <amount>, cat2: <amount>},
        Feb: {cat1: <amount>, cat2: <amount>}
    }}
    """
    year_v = year_transactions.keys()[0]
    print(year_v)
    year = PrettyTable()
    year.field_names = ["Category"]
    for monthname in year_transactions[year_v].keys():
        year.field_names.append(monthname)
    year.field_names.append("Total")
    year.field_names.append("Average")
    with open('nordea_categories.json', 'r') as handle:
        category_actors = json.load(handle)
    for category in category_actors.keys():
        line = [category]
        {cats[cat] if cat in cats.keys() else 0 for month, cats in year_transactions[year_v].items()}

