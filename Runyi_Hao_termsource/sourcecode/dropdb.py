import sqlite3

#drop any table after mistake
conn = sqlite3.connect('yelp.db')
cursor = conn.cursor()
cursor.execute('drop table business;')
conn.commit()
conn.close()