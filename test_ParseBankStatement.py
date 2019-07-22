import unittest
import os
from ParseBankStatement import get_csv_as_dict
PWD = os.path.dirname(os.path.realpath(__file__))

first_result = [{'date': '02.01.2019', 'amount': '-12,50', 'source': 'Oulun Suunnistus Ry'}
    ,{'date': '02.01.2019', 'amount': '-383,90', 'source': 'PAYTRAIL OYJ'}]

class TestParseBankStatement(unittest.TestCase):
    def test_get_csv_as_dict(self):
        self.assertEqual(get_csv_as_dict(os.path.join(PWD, 'unittest_data',
            'nordea_statement.csv')), first_result)
