import csv
import collections
import argparse
import json

with open('nordea_categories.json', 'r') as handle:
    CATEGORIES = json.load(handle)

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

def get_csv_as_dict(path_to_csv):
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

def check_category(source, categorize=True):
    """
    Check if source has an defined category.

    Params
    source  int     transaction source
    categorize  bool    If True, request category for not defined transaction
                        otherwise return category "Other" for those
    """
    other="Other"

    category = [key for key, value in CATEGORIES.items() if source in value]
    if category == []:
        if categorize:
            request = {str(i):key for i,key in enumerate(CATEGORIES.keys())}
            request["A"] = "ADD NEW CATEGORY"
            selection = input("For which category '{}' should be:{}".format(
                source, request
            ))
            if selection not in request.keys():
                print("Wrong selection! '{}' not in '{}'".format(
                    selection, request.keys()
                ))
                return check_category(source, categorize)
            elif selection == "A":
                new_category=input("Give new gategory name:")
                print("New category '{}' created".format(new_category))
                CATEGORIES[new_category] = []
                return new_category
            else:
                return request[selection]
    else:
        return category[0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse bank transactions')
    parser.add_argument('csvfile', type=str,
                        help='path to transaction csv file')
    args = parser.parse_args()
    csv = get_csv_as_dict(args.csvfile)
    for i, ta in enumerate(csv):
        category_known = [i for key, value in CATEGORIES.items() if ta in value]
        if category_known != []:
            continue
        category = check_category(source=ta['source'])
        print(category)
        CATEGORIES[category].append(ta['source'])
        if i == 10:
            break
    print(CATEGORIES)
    with open('cat_output.json', 'w') as handle:
        handle.write(json.dumps(CATEGORIES, indent=4, sort_keys=True))


