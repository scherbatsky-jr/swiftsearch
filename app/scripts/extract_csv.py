import csv
import mysql.connector
from datetime import datetime

connection = mysql.connector.connect(
    host='localhost',  # Name of the MySQL container in the Docker network
    port='10301',
    user='swiftsearch',
    password='swiftsearch',
    database='swiftsearch'
)

# Open the CSV file
with open('../data/japan_times.csv', mode='r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)
    i = 0
    for row in reader:
        if i > 0:
            try:
                cursor = connection.cursor()
                sql = "INSERT INTO sites (title, url, published_at, author, source, description, scraped_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (row[1], row[0], datetime.fromisoformat(row[5]), row[4], row[3], row[2], datetime.strptime(row[13], "%d/%m/%Y %H:%M:%S"))
                cursor.execute(sql, val)
                connection.commit()
                cursor.close()
            except Exception as e:
                print(e)
                continue
        i = i + 1
connection.close()