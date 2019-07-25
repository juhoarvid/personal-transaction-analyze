import csv
import collections
import argparse

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

def categorize_transaction(self, date, amount, source):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse bank transactions')
    parser.add_argument('csvfile', type=str,
                        help='path to transaction csv file')
    args = parser.parse_args()
    print(get_csv_as_dict(args.csvfile))


