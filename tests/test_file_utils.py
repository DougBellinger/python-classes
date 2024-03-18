import unittest
from python_classes.file_utils import open_csv_or_excel
import os
import logging

class TestFileUtils(unittest.TestCase):
    test_data = os.path.join(os.path.dirname(__file__), 'test_data')
    test1 = test_data+"/test1"
    @classmethod
    def setUpClass(cls):
        loglevel = logging.DEBUG
        logging.basicConfig(level=loglevel)
        cls.logger = logging.getLogger()
        cls.logger.debug("Setting up file_utils tests")
        if os.path.exists(cls.test1+".csv"):
            os.remove(cls.test1+'.csv')     

    def test_1_no_csv(self):
        self.logger.debug(f"Checking xlsx is present and csv is not ({self.test1})")
        self.assertTrue(os.path.isfile(self.test1+'.xlsx'), "missing test file test1.xlsx")
        self.assertFalse(os.path.isfile(self.test1+'.csv'), "csv file test1.csv is already there")

    def test_2_open_xlsx(self):
        self.logger.debug(f"Opening xlsx ({self.test1})")
        df = open_csv_or_excel(self.test1)
        (r,c) = df.shape
        self.assertEqual(r, 9, 'incorrect row count')
        self.assertEqual(c, 3, 'incorrect column count')

    def test_3_csv_created(self):
        csvfile = self.test1+'.csv'
        self.logger.debug(f"Checking CSV file ({os.path.abspath(csvfile)})")
        self.assertTrue(os.path.isfile(csvfile),"no csv file created")
        df = open_csv_or_excel(self.test1)
        (r,c) = df.shape
        self.assertEqual(r, 9, 'incorrect row count')
        self.assertEqual(c, 3, 'incorrect column count') # no extra column for index
        os.remove(self.test1+'.csv')
    
    
if __name__ == '__main__':
    unittest.main()