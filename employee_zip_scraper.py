import requests
import zipfile
import pandas as pd
import os
import time


class EmployeeZipScraper:

    def __init__(self, url):
        self.url = url
        self.zip_file = "employee_data.zip"
        self.extract_folder = "employee_files"

    def download_zip(self, retries=3):
        for attempt in range(retries):
            try:
                response = requests.get(self.url, timeout=30)
                response.raise_for_status()

                with open(self.zip_file, "wb") as file:
                    file.write(response.content)

                return self.zip_file

            except requests.RequestException as e:
                print(f"Download failed: {e}")

                if attempt < retries - 1:
                    print("Retrying...")
                    time.sleep(2)
                else:
                    raise Exception("Unable to download ZIP file.")

    def extract_zip(self):
        try:
            with zipfile.ZipFile(self.zip_file, "r") as zip_ref:
                zip_ref.extractall(self.extract_folder)

            for file in os.listdir(self.extract_folder):
                if file.endswith(".xlsx") or file.endswith(".xls"):
                    return os.path.join(self.extract_folder, file)

            raise Exception("No Excel file found.")

        except zipfile.BadZipFile:
            raise Exception("Invalid ZIP file.")

    def validate_file(self, excel_file):
        if not (excel_file.endswith(".xlsx") or excel_file.endswith(".xls")):
            raise Exception("Unsupported file format.")

        try:
            df = pd.read_excel(excel_file)
            df[["First Name","Last Name"]]=df["Full Name"].str.split(" ",n=1,expand=True)
            df.rename(columns={"EEID":"Employee ID"},inplace=True)
            return df
        except Exception as e:
            raise Exception(f"Error reading Excel file:{e}")

    def validate_data(self, df):

        required_columns = [
            "Employee ID",
            "First Name",
            "Last Name",
            "Job Title",
            "Hire Date",
            "Department",
            "Business Unit",
            "Annual Salary",
            "Gender",
            "Ethnicity",
            "Age",
            "Bonus %",
            "Country",
            "City"
            
        ]
        if df[required_columns].isnull().values.any():
            print("Missing values detected in the following columns:")
            print(df.isnull().sum()[df.isnull().sum()>0])
        else:
            print("Data validation completed successfully.")
        
        for column in required_columns:
            if column not in df.columns:
                raise Exception(f"Missing column: {column}")

        return True


if __name__ == "__main__":

    url = "https://www.thespreadsheetguru.com/wp-content/uploads/2022/12/EmployeeSampleData.zip"

    scraper = EmployeeZipScraper(url)

    scraper.download_zip()
    excel = scraper.extract_zip()
    dataframe = scraper.validate_file(excel)
    scraper.validate_data(dataframe)
    print(dataframe[
                [
                    "Employee ID",
                    "First Name",
                    "Last Name",
                    "Job Title",
                    "Hire Date",
                    "Department",
                    "Business Unit",
                    "Annual Salary",
                    "Gender",
                    "Ethnicity",
                    "Age",
                    "Bonus %",
                    "Country",
                    "City"
                ]
    ])
    