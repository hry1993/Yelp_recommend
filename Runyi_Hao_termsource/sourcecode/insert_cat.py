import csv
import sqlite3
import re

# map and insert category
n=1
conn = sqlite3.connect('yelp.db')
cursor = conn.cursor()
with open('./yelp_business.csv','r',encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        category_set = re.split(';',row['categories'])
        if 'Restaurants' in category_set or 'Bars' in category_set or 'Food' in category_set:
            for i in range(len(category_set)):
                cursor.execute('INSERT INTO category values (?,?,?);',(n,row['business_id'],category_set[i]))
                n=n+1
        else:
            continue
    conn.commit()
file.close()
conn.commit()
conn.close()