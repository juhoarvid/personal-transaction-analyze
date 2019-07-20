import unittest
import os
from ParseBankStatement import get_csv_as_dict
PWD = os.path.dirname(os.path.realpath(__file__))

class TestParseBankStatement(unittest.TestCase):
    def test_get_csv_as_dict(self):
        self.assertEqual(get_csv_as_dict(os.path.join(PWD, 'unittest_data',
            'nordea_statement.csv')), None)
