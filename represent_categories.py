import json
from collections import OrderedDict
from prettytable import PrettyTable

class Month(object):
    def __init__(self, conf_file_path):
        with open(conf_file_path, 'r') as handle:
            parsed = json.load(handle)
        self.__dict__.update({category:0 for category,_ in parsed.items()})

    def get_month_total(self):
        return sum([value for key, value in self.__dict__.items()])

class Year(object):
    def __init__(self, conf_file_path, yearname):
        with open(conf_file_path, 'r') as handle:
            parsed = json.load(handle)
        self.categories = {cat:{"total":0, "avg":0} for cat,_ in parsed.items()}
        self.months = OrderedDict()
        self.yearname = yearname

    def print(self):
        if self.months == {}:
            return True
        year = PrettyTable()
        
        field_names = ["Category"]
        for monthname in self.months.keys():
            field_names.append(monthname)
        field_names.append("TOTAL")
        field_names.append("AVG")
        year.field_names = field_names
        year.title = "upper"

        for category in self.categories.keys():
            line = [category]
            category_values = []
            for month in self.months.keys():
                category_values.append(int(self.months[month].__dict__[category]))
            total = sum(category_values)

            line.extend(category_values)
            line.append(int(total))
            if len(category_values) > 0:
                avg=int(total/len(category_values))
            else:
                avg=0
            self.categories[category]["total"] = total
            self.categories[category]["avg"] = avg
            line.append(avg)
            year.add_row(line)
        totals =["TOTAL"]
        for month in self.months.keys():
            totals.append(int(self.months[month].get_month_total()))
        totals.append(sum([value['total'] for category, value in self.categories.items()]))
        totals.append(sum([value['avg'] for category, value in self.categories.items()]))
        year.add_row(totals)
        year.align = 'l'

        import prettytable, os
        year.right_padding_width = 0

        year_str = str(year.get_string(title=self.yearname))
        print("{}".format(year_str))