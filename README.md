Employee Data ZIP Scraper

Overview
This project downloads employee data from a ZIP file URL, extracts the Excel file, validates its format, reads employee information, and performs data validation. It also includes automated unit tests to verify the scraper functionality.

 Features
- Download ZIP file from a URL
- Extract ZIP archive
- Validate Excel file format
- Read employee data
- Validate employee information
- Handle download and extraction errors
- Unit testing using unittest

Technologies Used:
- Python
- Requests
- Pandas
- ZipFile
- unittest


Install:

pip install -r requirements.txt


Run the scraper:

python employee_zip_scraper.py


Run the tests:

python -m unittest test_employee_zip_scraper.py




