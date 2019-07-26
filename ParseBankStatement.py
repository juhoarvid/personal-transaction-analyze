import csv
import collections
import optparse
import json
import represent_categories



class NordeaTransactionLine(object):
    def __init__(self, Kirjauspaiva, Arvopaiva, Maksupaiva, Maara,
        SaajaMaksaja, Tilinumero, BIC, Tapahtuma, Viite,
        MaksajanViite, Viesti, Kortinnumero, Kuitti, *args):
        self.date = Kirjauspaiva
        self.amount = Maara
        self.source = SaajaMaksaja

conf = {
    'nordea' : {
        'first_transaction_line' : 5,
        'transcation_field_parser' : NordeaTransactionLine
    }
}
class categorize(object):
    conf = {
        'nordea' : {
            'first_transaction_line' : 5,
            'transcation_field_parser' : NordeaTransactionLine,
            'timestampformat' : '%d.%m.%Y'
        }
    }
    def __init__(self, categoryinputfile):
        with open(categoryinputfile, 'r') as handle:
            self.CATEGORIES = json.load(handle)

    def get_csv_as_dict(self, path_to_csv):
        csv_list = []
        with open(path_to_csv, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            csvline=1
            for row in csv_reader:
                if csvline < conf['nordea']['first_transaction_line']:
                    csvline+=1
                    continue
                try:
                    csv_list.append(((conf['nordea']['transcation_field_parser'](*row).__dict__)))
                except TypeError:
                    if row != []:
                        print("PASS:{}".format(row))
                    pass
        return csv_list

    def check_category(self, source, categorize=True):
        """
        Check if source has an defined category.

        Params
        source  int     transaction source
        categorize  bool    If True, request category for not defined transaction
                            otherwise return category "Other" for those
        """
        other="Other"

        category = [key for key, value in self.CATEGORIES.items() if source in value]
        if category == []:
            if categorize:
                request = {str(i):key for i,key in enumerate(self.CATEGORIES.keys())}
                request["A"] = "ADD NEW CATEGORY"
                selection = input("For which category '{}' should be:{}".format(
                    source, request
                ))
                if selection not in request.keys():
                    print("Wrong selection! '{}' not in '{}'".format(
                        selection, request.keys()
                    ))
                    return self.check_category(source, categorize)
                elif selection == "A":
                    new_category=input("Give new gategory name:")
                    print("New category '{}' created".format(new_category))
                    self.CATEGORIES[new_category] = []
                    return new_category
                else:
                    return request[selection]
        else:
            return category[0]

if __name__ == '__main__':
    parser = optparse.OptionParser(description='Parse bank transactions')
    parser.add_option('-c', '--configuration', action='store',
                        dest='configurationfilepath',
                        default="nordea_categories.json",
                        help='configuration file')
    parser.add_option('-i', '--input', action='store',
                        dest='inputfile',
                        help='Transaction csv file path')
    parser.add_option('-o', '--output', action='store',
                        dest='outputcatfile',
                        default="nordea_categories.json",
                        help='New categories will be added to this file')
    (options, args) = parser.parse_args()
    cat = categorize(options.configurationfilepath)
    csv = cat.get_csv_as_dict(options.inputfile)
    for i, ta in enumerate(csv):
        category_known = [key for key, value in cat.CATEGORIES.items() if ta['source'] in value]
        if category_known is not []:
            continue
        category = cat.check_category(source=ta['source'])
        print(category)
        cat.CATEGORIES[category].append(ta['source'])
        if i == 10:
            break
    print(cat.CATEGORIES)
    with open(options.outputcatfile, 'w') as handle:
        handle.write(json.dumps(cat.CATEGORIES, indent=4, sort_keys=True))

    ### PARSE TRANSACTION TO TIME
    from datetime import datetime
    years = {}
    for transaction in csv:
        action_time = datetime.strptime(transaction["date"], cat.conf["nordea"]["timestampformat"])
        ta_year = action_time.strftime("%Y")
        ta_month = action_time.strftime("%m")
        if ta_year not in years.keys():
            years[ta_year] = represent_categories.Year()
        if ta_month not in years[ta_year].months.keys():
            years[ta_year].months[ta_month] = represent_categories.Month()
        ta_category = [key for key, value in cat.CATEGORIES.items() if transaction['source'] in value][0]
        print(ta_category)
        catsum=years[ta_year].months[ta_month].__dict__[ta_category]
        catsum = float(catsum) + float(transaction['amount'].replace(',','.'))
        years[ta_year].months[ta_month].__dict__[ta_category] = catsum
    for year in years.keys():
        print(year)
        years[year].print()

        


