import sqlite3
import csv
import os

# Paths
db_path = os.path.abspath("local_data/database/Database.db")
csv_path = os.path.abspath("C:/Users/Windows/Desktop/Crisma Manager/utilities/random_items.csv")

# Connect to the database
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Open and read the CSV file
with open(csv_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip the header row

    # Insert each row into the ITEM table
    for row in reader:
        try:
            query = """INSERT INTO ITEM (NAME, REFERENCE, CODE, LINE, CAPACITY, QUANTITY, IMAGE) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, row)
        except Exception as e:
            print(f"Error adding row {row}: {e}")

# Commit changes and close the connection
connection.commit()
connection.close()

print("Data added to the ITEM table successfully.")
