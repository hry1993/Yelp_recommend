import csv
import sqlite3
import re

#insert user data
csv.field_size_limit(100000000)
conn = sqlite3.connect('yelp.db', timeout=10) #disconnect auto
cursor = conn.cursor()
with open('./yelp_user.csv','r',encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('INSERT INTO user values (?,?,?);',(row['user_id'],row['name'],row['friends']))
    conn.commit()
file.close()
conn.commit()
conn.close()