import csv
import sqlite3

#insert business data
conn = sqlite3.connect('yelp.db')
cursor = conn.cursor()
with open('./yelp_business.csv','r',encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('INSERT INTO business values (?,?,?,?,?,?,?,?);',(row['business_id'],row['name'],row['address'],row['city'],row['state'],row['postal_code'],row['stars'],row['review_count']))
    conn.commit()
file.close()
conn.commit()
conn.close()