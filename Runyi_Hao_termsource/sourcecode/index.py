import sqlite3

#create index
conn = sqlite3.connect('yelp.db')
cursor = conn.cursor()
#cursor.execute('drop index user_index;')
#cursor.execute('drop index tip_index;')
#cursor.execute('drop index business_index;')
#cursor.execute('drop index category_index;')
#cursor.execute('drop index review_index;')
cursor.execute('create index user_index on user(user_id);')
cursor.execute('create index tip_index on tip(business_id);')
cursor.execute('create index business_index on business(business_id,city,state,postal,stars,review_count);')
cursor.execute('create index category_index on category(business_id,category);')
cursor.execute('create index review_index on review(business_id,user_id,stars);')
conn.commit()
conn.close()