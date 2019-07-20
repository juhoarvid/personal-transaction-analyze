import csv

def get_csv_as_dict(path_to_csv):
    with open(path_to_csv, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            try:
                print(NordeaTransactionLine(*row))
                print(NordeaTransactionLine(*row).__dict__)
            except TypeError:
                print("PASS:{}".format(row))
                pass


class NordeaTransactionLine(object):
    def __init__(self, Kirjauspaiva, Arvopaiva, Maksupaiva, Maara,
        SaajaMaksaja, Tilinumero, BIC, Tapahtuma, Viite,
        MaksajanViite, Viesti, Kortinnumero, Kuitti, *args):
        self.Kirjauspaiva = Kirjauspaiva
        self.Maara = Maara
        self.SaajaMaksaja = SaajaMaksaja

    def __str__(self):
        return "{}:{}:{}".format(self.Kirjauspaiva, self.Maara, self.SaajaMaksaja)