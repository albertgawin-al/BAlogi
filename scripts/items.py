import csv
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('serviceKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define a function to convert column types with null handling
def convert_types(row):
    row['#'] = int(row['#']) if row['#'] else None
    row['I'] = str(row['I']) if row['I'] else None
    row['C'] = str(row['C']) if row['C'] else None
    row['Name'] = str(row['Name']) if row['Name'] else None
    row['Nickname'] = str(row['Nickname']) if row['Nickname'] else None
    row['SubType'] = str(row['SubType']) if row['SubType'] else None
    row['Ammo'] = str(row['Ammo']) if row['Ammo'] else None
    row['Faction'] = str(row['Faction']) if row['Faction'] else None
    row['StockpileCategory'] = str(row['StockpileCategory']) if row['StockpileCategory'] else None
    row['CategorySort'] = int(row['CategorySort']) if row['CategorySort'] else None
    row['InCategorySort'] = int(row['InCategorySort']) if row['InCategorySort'] else None
    row['IndExists'] = int(row['IndExists']) if row['IndExists'] else None
    row['CrateExists'] = int(row['CrateExists']) if row['CrateExists'] else None
    row['perCrate'] = int(row['perCrate']) if row['perCrate'] else None
    row['Bmats'] = int(row['Bmats']) if row['Bmats'] else None
    row['Emats'] = int(row['Emats']) if row['Emats'] else None
    row['Rmats'] = int(row['Rmats']) if row['Rmats'] else None
    row['Hemats'] = int(row['Hemats']) if row['Hemats'] else None
    row['Relicmats'] = int(row['Relicmats']) if row['Relicmats'] else None

    return row

# Read CSV file and convert to JSON
csv_file_path = 'ItemNumbering.csv'
json_data = []

with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        converted_row = convert_types(row)
        json_data.append(converted_row)

# Send JSON data to Firebase
collection_name = 'item'  # Specify your collection name
for item in json_data:
    db.collection(collection_name).add(item)

print("Data successfully sent to Firebase.")