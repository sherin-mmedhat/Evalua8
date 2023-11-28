# Import the python libraries
import csv
from pymongo import MongoClient
from pprint import pprint

# Choose the appropriate client
client = MongoClient()

# Connect to the test db 
db=client.KPI

# Use the KPI collection
KPI = db.kpi_collection

# Delte all for testing, multi run
result = KPI.delete_many({})

# Specify the path to your CSV file
csv_file_path = 'data/profiling/KPI.csv'

# Read data from CSV file
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data_to_insert = list(csv_reader)

# Insert data into MongoDB
result = KPI.insert_many(data_to_insert)

# Find documents where ...
projection = {'KPI': 1, '_id': 0}
query = {"Engineering_manager": "Yes", "Job_title": "Senior Software Engineer"}
kpi_data_list = list(KPI.find(query, projection))
pprint(kpi_data_list)
