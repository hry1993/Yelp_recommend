import csv
import sqlite3
import re

#insert review data
conn = sqlite3.connect('yelp.db', timeout=10)
cursor = conn.cursor()
with open('./yelp_review.csv','r',encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('INSERT INTO review values (?,?,?);',(row['business_id'],row['user_id'],row['stars']))
    conn.commit()
file.close()
conn.commit()
conn.close()