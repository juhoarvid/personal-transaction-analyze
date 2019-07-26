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
        
        field_names = ["Category"]
        for monthname in self.months.keys():
            field_names.append(monthname)
        field_names.append("Total")
        field_names.append("Average")
        year.field_names = field_names
        
        for category in self.categories:
            line = [category]
            category_values = []
            for month in self.months.keys():
                category_values.append(self.months[month].__dict__[category])
            line.extend(category_values)
            line.append(sum(category_values))
            if len(category_values) > 0:
                avg=int(sum(category_values)/len(category_values))
            else:
                avg=0
            line.append(avg)
            year.add_row(line)
        print(year)