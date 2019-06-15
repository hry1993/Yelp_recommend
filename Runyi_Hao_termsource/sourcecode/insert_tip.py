import csv
import sqlite3
import re
#insert tip data
n=1
conn = sqlite3.connect('yelp.db', timeout=10)
cursor = conn.cursor()
with open('./yelp_tip.csv','r',encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute('INSERT INTO tip values (?,?,?);',(n,row['business_id'],row['text']))
        n=n+1
    conn.commit()
file.close()
conn.commit()
conn.close()