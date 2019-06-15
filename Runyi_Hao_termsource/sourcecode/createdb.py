import sqlite3

#create sqlite database
conn = sqlite3.connect('yelp.db')
cursor = conn.cursor()
cursor.execute('create table user (user_id text, name text, friend_id text);')
cursor.execute('create table review (business_id text, user_id text, stars number);')
cursor.execute('create table tip (tip_id int, business_id text, tip text);')
cursor.execute('create table business (business_id text, name text, address text, city text, state text, postal text, stars number, review_count int);')
cursor.execute('create table category (category_id int, business_id text, category text);')
conn.commit()
conn.close()