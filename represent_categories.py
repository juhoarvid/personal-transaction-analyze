import json
from collections import OrderedDict
from prettytable import PrettyTable

class Month(object):
    def __init__(self):
        with open('nordea_categories.json', 'r') as handle:
            parsed = json.load(handle)
        self.__dict__.update({category:0 for category,_ in parsed.items()})

class Year(object):
    def __init__(self):
        with open('nordea_categories.json', 'r') as handle:
            parsed = json.load(handle)
        self.categories = [cat for cat,_ in parsed.items()]
        self.months = OrderedDict()

    def print(self):
        if self.months == {}:
            return True
        year = PrettyTable()
        year.field_names = ["Category"]
        for monthname in self.months.keys():
            year.field_names.append(monthname)
        year.field_names.append("Total")
        year.field_names.append("Average")
        
        for category in self.categories:
            line = [category]
            category_values = []
            for month in self.months.keys():
                category_values.append(self.months[month][category])
            line.extend(category_values)
            line.append(tot(category_values))
            line.append(int(tot(category_values)/len(category_values)))
            year.add_row(line)
        print(year)