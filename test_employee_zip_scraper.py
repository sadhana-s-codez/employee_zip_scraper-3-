import unittest
import pandas as pd
from employee_zip_scraper import EmployeeZipScraper


URL = "https://www.thespreadsheetguru.com/wp-content/uploads/2022/12/EmployeeSampleData.zip"


class TestEmployeeZipScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = EmployeeZipScraper(URL)

    
    def test_download_zip(self):
        file = self.scraper.download_zip()
        self.assertTrue(file.endswith(".zip"))

   
    def test_extract_zip(self):
        self.scraper.download_zip()
        excel = self.scraper.extract_zip()
        self.assertTrue(excel.endswith(".xlsx") or excel.endswith(".xls"))

   
    def test_validate_file_type(self):
        self.scraper.download_zip()
        excel = self.scraper.extract_zip()
        df = self.scraper.validate_file(excel)
        self.assertIsInstance(df, pd.DataFrame)

   
    def test_validate_data_structure(self):
        self.scraper.download_zip()
        excel = self.scraper.extract_zip()
        df = self.scraper.validate_file(excel)
        self.assertTrue(self.scraper.validate_data(df))

    
    def test_missing_invalid_data(self):
        data = {
            "Employee ID": [1],
            "First Name": ["John"]
        }

        df = pd.DataFrame(data)

        with self.assertRaises(Exception):
            self.scraper.validate_data(df)


if __name__ == "__main__":
    unittest.main()