from tkinter import *
from numpy import *
import svd
import dataselect
import random
import sqlite3

category_set=[]
tip_set=[]
userid='1'
postalcode='123'
businessid=[]
#input review
def quit(getscore,bid,userid):
    conn = sqlite3.connect('yelp.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO review values(?,?,?)', (bid, userid, getscore.get()))
    conn.commit()
    conn.close()
    root.quit()
#get SVD recommend choice chosen. ask for review
def select(bid):
    global userid,businessid
    for i in range(len(businessid)):
        exec('result'+str(i)+'.pack_forget()')
    conn = sqlite3.connect('yelp.db')
    cursor = conn.cursor()
    cursor.execute('select name,address,city,state,postal from business where business_id=?;', (bid,))
    for row in cursor.fetchall():
        result1text = 'name: ' + row[0] + ' address: ' + row[1] + ' city: ' + row[2] + ' state: ' + row[3] + ' postal ' + row[4]
        res = Label(root, text=result1text)
        res.pack()
    conn.commit()
    conn.close()
    score = StringVar()
    getscore = Entry(root, textvariable=score)
    score.set('evaluate from 0 to 5.0')
    getscore.pack()
    submit=Button(root,text='submit score', command=lambda: quit(getscore,bid,userid))
    submit.pack()
#get tip chocie chosen, recommend and ask for review
def selecttip(bid):
    global userid,button1,button2,button3,button4,button5,reroll2
    button1.pack_forget()
    button2.pack_forget()
    button3.pack_forget()
    button4.pack_forget()
    button5.pack_forget()
    reroll2.pack_forget()
    conn = sqlite3.connect('yelp.db')
    cursor = conn.cursor()
    cursor.execute('select name,address,city,state,postal from business where business_id=?;', (bid,))
    for row in cursor.fetchall():
        target = 'name: ' + row[0] + ' address: ' + row[1] + ' city: ' + row[2] + ' state: ' + row[3] + ' postal ' + \
                 row[4]
        res = Label(root, text=target)
        res.pack()
    conn.commit()
    conn.close()
    score = StringVar()
    getscore = Entry(root, textvariable=score)
    score.set('evaluate from 0 to 5.0')
    getscore.pack()
    submit = Button(root, text='submit score', command=lambda: quit(getscore, bid, userid))
    submit.pack()
#refresh tip choices
def refresh2(tip_set):
    global randomtip
    number = [random.randint(0, len(tip_set)) for _ in range(5)]
    button1['text'] = tip_set[number[0]][0]
    button2['text'] = tip_set[number[1]][0]
    button3['text'] = tip_set[number[2]][0]
    button4['text'] = tip_set[number[3]][0]
    button5['text'] = tip_set[number[4]][0]
#create tip choices
def tips():
    global businessid,tip_set,button1,button2,button3,button4,button5,reroll2
    conn = sqlite3.connect('yelp.db')
    cursor = conn.cursor()
    for i in range(len(businessid)):
        cursor.execute('SELECT tip FROM tip where business_id=?;',(businessid[i],))
        for row in cursor.fetchall():
            tipcurrentset=re.split(',.?"!', row[0])
            for j in range(len(tipcurrentset)):
                med=[tipcurrentset[j],businessid[i]]
                tip_set.append(med)
    conn.commit()
    conn.close()
    randomtip = [random.randint(0, len(tip_set)) for _ in range(5)]
    button1 = Button(root, text=tip_set[randomtip[0]][0], command=lambda: selecttip(tip_set[randomtip[0]][1]))
    button1.pack()
    button2 = Button(root, text=tip_set[randomtip[1]][0], command=lambda: selecttip(tip_set[randomtip[1]][1]))
    button2.pack()
    button3 = Button(root, text=tip_set[randomtip[2]][0], command=lambda: selecttip(tip_set[randomtip[2]][1]))
    button3.pack()
    button4 = Button(root, text=tip_set[randomtip[3]][0], command=lambda: selecttip(tip_set[randomtip[3]][1]))
    button4.pack()
    button5 = Button(root, text=tip_set[randomtip[4]][0], command=lambda: selecttip(tip_set[randomtip[4]][1]))
    button5.pack()
    reroll2 = Button(root, text='reroll', command=lambda: refresh2(tip_set))
    reroll2.pack()
#create choices according to category
def third(cate):
    global postalcode,businessid
    conn = sqlite3.connect('yelp.db')
    cursor = conn.cursor()
    cursor.execute('SELECT business.business_id FROM category join business on category.business_id=business.business_id where substr(business.postal,1,3)=? and category.category=?;',(postalcode,cate))
    for row in cursor.fetchall():
        businessid.append(row[0])
    conn.commit()
    conn.close()
    button1.pack_forget()
    button2.pack_forget()
    button3.pack_forget()
    button4.pack_forget()
    button5.pack_forget()
    if len(businessset) >= 3:
        button6.pack_forget()
    reroll1.pack_forget()
    #if result more than 5, filter by tip again
    if len(businessid) > 5:
        tips()
    else:
    #if result less than 5, output result
        conn = sqlite3.connect('yelp.db')
        cursor = conn.cursor()
        for i in range(len(businessid)):
            cursor.execute('select name,address,city,state,postal from business where business_id=?;',(businessid[i],))
            for row in cursor.fetchall():
                result1text='name: '+row[0]+' address: '+row[1]+' city: '+row[2]+' state: '+row[3]+' postal '+row[4]
                globals()['result'+str(i)]=Button(root,text=result1text,command=lambda: select(businessid[i]))
                exec('result'+str(i)+'.pack()')
        conn.commit()
        conn.close()
#random category choices
def refresh1(category_set):
    global number
    number = [random.randint(0, len(category_set)) for _ in range(5)]
    button1['text']=category_set[number[0]]
    button2['text'] = category_set[number[1]]
    button3['text'] = category_set[number[2]]
    button4['text'] = category_set[number[3]]
    button5['text'] = category_set[number[4]]

def recommend(uid):
    #create array
    data = (dataselect.recommend2(uid, dataselect.recommend1(uid)))
    #get score
    resultset=svd.recommend(mat(data), 5, 0.9)
    global businessid
    businessid=[]
    #drop old GUI
    button1.pack_forget()
    button2.pack_forget()
    button3.pack_forget()
    button4.pack_forget()
    button5.pack_forget()
    button6.pack_forget()
    reroll1.pack_forget()
    #select and show results
    conn = sqlite3.connect('yelp.db')
    cursor = conn.cursor()
    for i in range(len(resultset)):
        businessid.append(dataselect.newbusiness[resultset[i][0]])
    for i in range(len(resultset)):
        cursor.execute('select name,address,city,state,postal from business where business_id=?;', (businessid[i],))
        for row in cursor.fetchall():
            result1text = 'name: ' + row[0] + ' address: ' + row[1] + ' city: ' + row[2] + ' state: ' + row[
                3] + ' postal ' + row[4] +' Score:' + str(resultset[i][1])
            globals()['result' + str(i)] = Button(root, text=result1text, command=lambda: select(businessid[i]))
            exec('result' + str(i) + '.pack()')
    conn.commit()
    conn.close()

def second(user_id,postal_code):
    global userid,postalcode,button1,button2,button3,button4,button5,button6,reroll1,businessset
    #convert input
    userid=user_id.get()
    postalcode=postal_code.get()
    #select using postal
    conn = sqlite3.connect('yelp.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category FROM category join business on category.business_id=business.business_id where substr(business.postal,1,3)=?;',(postalcode,))
    for row in cursor.fetchall():
        if row[0] not in category_set and row[0] != 'Food' and row[0] != 'Restaurants':
            category_set.append(row[0])
    #drop old GUI
    postal.pack_forget()
    user.pack_forget()
    next_step.pack_forget()
    #create choices
    number = [random.randint(0, len(category_set)) for _ in range(5)]
    button1 = Button(root, text=category_set[number[0]], command=lambda: third(category_set[number[0]]))
    button1.pack()
    button2 = Button(root, text=category_set[number[1]], command=lambda: third(category_set[number[0]]))
    button2.pack()
    button3 = Button(root, text=category_set[number[2]], command=lambda: third(category_set[number[0]]))
    button3.pack()
    button4 = Button(root, text=category_set[number[3]], command=lambda: third(category_set[number[0]]))
    button4.pack()
    button5 = Button(root, text=category_set[number[4]], command=lambda: third(category_set[number[0]]))
    button5.pack()
    #reroll button
    reroll1 = Button(root, text='reroll', command=lambda: refresh1(category_set))
    reroll1.pack()
    businessset = []
    cursor.execute('select business_id from review where user_id=?', (userid,))
    for row in cursor.fetchall():
        businessset.append(row[0])
    conn.close()
    #if user's reviews > 3 show recommend button
    if len(businessset) >= 3:
        button6 = Button(root, text='recommend', command=lambda: recommend(userid))
        button6.pack()

#main
#create GUI
root= Tk()
root.title('Food recommend')
root.geometry()
#get input
user_id=StringVar()
user=Entry(root,textvariable=user_id)
user_id.set('input your user id here')
user.pack()

postal_code=StringVar()
postal=Entry(root,textvariable=postal_code)
postal_code.set('input first three digits of the postal here')
postal.pack()
#submit input
next_step=Button(root, text='next', command= lambda: second(user_id,postal_code))
next_step.pack()
#refresh GUI
root.mainloop()