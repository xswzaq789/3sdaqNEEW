import sqlite3
con = sqlite3.connect('db.sqlite3')
print("^^")
cur = con.cursor()
#cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

from datetime import datetime
import time
'''
now = datetime.datetime.now()
print(now)          # 2015-04-19 12:11:32.669083

nowDate = now.strftime('%Y-%m-%d')
print(nowDate)      # 2015-04-19
nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
print(nowDatetime)  # 2015-04-19 12:11:32
'''
now = datetime.now()
nowTime = now.strftime('%H:%M:%S')
#print(nowTime)      # 12:11:32
#print(type(nowTime))      # 12:11:32

not_insert = True
point_time = "15:13:30"
'''
while (not_insert):
        now2 = datetime.now()
        nowTime = now2.strftime('%H:%M:%S')
        if(nowTime > point_time):
                print("execute time : ", nowTime)
                for row in cur.execute('select * from bbsApp_webBbs '):
                        print(row)
                sql_insert = ""
                sql_insert += "insert into bbsApp_webbbs(title, writer, content, regdate, viewcnt)"
                sql_insert += "values('test2', 'minsu', '테스트', (select datetime('now', 'localtime')), 0)"
                print(sql_insert)
                cur.execute(sql_insert)
                not_insert = False
        else:
                time_1 = datetime.strptime(point_time, "%H:%M:%S")
                time_interval = time_1 - (now2.strptime(nowTime, '%H:%M:%S'))
                print("Now time : ", nowTime, " 남은시간" , time_interval)
                time.sleep(5)

'''
print("not_insert : ", not_insert)
query_txt = ""
query_txt += " insert into tradeApp_order(code, gubun, price, quan, tquan, buyer, tradeyn, time1)"
query_txt += " values(1,'B', 72000, 20, 0, 'minsu', 'N', (select datetime('now','localtime')))"
cur.execute(query_txt)

con.commit()

#
# import random
#
# foo = ['a', 'b', 'c', 'd', 'e']
# print(random.choice(foo))
#
# import random
# mylist = ["apple", "banana", "cherry"]
# print(random.choices(mylist, cum_weights=[10, 5, 1], k=9))


con.close()