import sqlite3
import random

global newbusiness
#error treat
class baddata(Exception):
    pass
#check the number of business that user has rated and distribute to different process
def recommend1(uid):
    businessset=[]
    conn=sqlite3.connect('yelp.db')
    cursor=conn.cursor()
    cursor.execute('select business_id from review where user_id=?',(uid,))
    for row in cursor.fetchall():
        businessset.append(row[0])
    conn.close()
    # <3 can not use SVD
    if len(businessset)<3:
        raise baddata
    # 3-6 use SVD
    elif 3<=len(businessset)<=6:
        return businessset
    # >6 randome choose 6 to use SVD
    elif len(businessset)>6:
        randombusiness = random.sample(businessset,6)
        return randombusiness

def recommend2(uid,businessset):
    userset=[]
    newbusinessset={}
    conn = sqlite3.connect('./yelp.db')
    cursor = conn.cursor()
    #get userid that has rated the business got in previous steps
    for i in range(len(businessset)):
        cursor.execute('select user_id from review where business_id=?', (businessset[i],))
        for row in cursor.fetchall():
            if row[0] not in userset and row[0]!=uid:
                userset.append(row[0])
    #choose 10 from them
    if len(userset)>10:
        userset = random.sample(userset, 10)
    #map reduce to get the business rated most
    for i in range(len(userset)):
        cursor.execute('select business_id from review where user_id=?', (userset[i],))
        for row in cursor.fetchall():
            if row[0] not in businessset and row[0] not in newbusinessset:
                newbusinessset[row[0]]=1
            if row[0] in newbusinessset:
                newbusinessset[row[0]]+=1
    newbusinesssort=[key for key,value in sorted(newbusinessset.items(), key=lambda d: d[1], reverse=True)]
    print(newbusinessset)
    times=0
    global newbusiness
    newbusiness=businessset
    stop=(len(businessset)+6)
    #filter business gotten, get business that other user rated most, but user has not rated
    for times in range(len(newbusinesssort)):
        cursor.execute('select stars from review where business_id=? and user_id=?', (newbusinesssort[times],uid))
        answer=cursor.fetchall()
        if len(answer)==0:
            newbusiness.append(newbusinesssort[times])
        if len(newbusiness) >= stop:
            break
    #create list for storing array,default 0
    data=[[0 for x in range(len(newbusiness))] for y in range(len(userset)+1)]
    #get score for each slot, if exists input, not exists keep 0
    for i in range(len(newbusiness)):
        try:
            cursor.execute('select stars from review where business_id=? and user_id=?', (newbusiness[i], uid))
            for row in cursor.fetchall():
                data[0][i]=row[0]
        except:
            pass
    for i in range(len(newbusiness)):
        for n in range(len(userset)):
            try:
                cursor.execute('select stars from review where business_id=? and user_id=?', (newbusiness[i], userset[n]))
                for row in cursor.fetchall():
                    data[n+1][i] = row[0]
            except:
                pass
    conn.close()
    print(data)
    return data

