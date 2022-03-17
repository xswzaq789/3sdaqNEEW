import os
import random
import sys
import sqlite3
from random import sample, randrange
from math import floor
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request as req

'''
 sqlite 위치 
'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR : ", BASE_DIR)
dbURL = os.path.join(BASE_DIR , 'db.sqlite3')
print("dbURL : ", dbURL)
tradeAppURL = os.path.join(BASE_DIR , 'tradeApp')
print("tradeAppURL : " , tradeAppURL)
sys.path.append(tradeAppURL)

print(BASE_DIR)
con = sqlite3.connect(dbURL)

from views import query_market_price


def bbs_update():
    con = sqlite3.connect(dbURL)
    cur = con.cursor()
    '''
    response = requests.get("https://finance.naver.com/news/mainnews.naver")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select(".articleSubject")
    fdic = {}
    title = []
    url = []
    for link in links:
        x = 'http://finance.naver.com' + link.find('a')['href'].strip()
        url.append(x)
        y = link.text.strip()
        title.append(y)
    for i in range(len(links)):
        fdic[i] = [title[i], url[i]]
    print('실행중')
    
    cur = con.cursor()
    for i in fdic:
        title = fdic[i][0]
        url = fdic[i][1]
        sql = "insert into userApp_sbs values(?,?,?)"
        cur.execute(sql, (title, url))
        
    '''

    url = "https://news.daum.net/"
    # url 열기
    target = req.urlopen(url)
    # 데이터 분석하기
    soup = BeautifulSoup(target, "html.parser")
    #file = open("news.txt", "w")
    news = soup.select("strong.tit_g")
    print("len(news) : ", len(news))
    if(len(news) > 5):
        sql_delete = "delete from userApp_sbs"
        cur.execute(sql_delete)
        con.commit()
        sql_update = "update sqlite_sequence set seq = 0 where name = 'userApp_sbs'"
        cur.execute(sql_update)
        con.commit()
        for list in news:
            a = list.select_one("a")
            print("링크 : " + a.get('href'))
            title = a.string
            print("제목 : " + title.strip())
            sql_insert_news = "insert into userApp_sbs(title, url) values(?,?)"
            cur.execute(sql_insert_news, (title.strip(), a.get('href').strip()))

        con.commit()
        con.close()

def insert_daily_prices_closing(market_price, d_day):
    con = sqlite3.connect(dbURL)
    cur = con.cursor()
    new_market_price = []
    for i in market_price:
        new_market_price.append((i['code'], i['name'], i['price']))
    #print(new_market_price)
    sql_insert = ""
    sql_insert += "insert OR REPLACE into tradeApp_d_price(day, code, name, price, regdate)"
    #sql_insert += "values((select strftime('%Y-%m-%d', 'now', 'localtime', '"+d_day+"')),?,?,?,(select datetime('now', 'localtime', '"+d_day+"')))"
    sql_insert += "values((select strftime('%Y-%m-%d', 'now', 'localtime', '" + d_day + "')), ?, ?, ?, (select datetime('now', 'localtime', '" + d_day + "')))"
    # print(sql_insert)
    cur.executemany(sql_insert, new_market_price)

    new_market_price = []
    for i in market_price:
        new_market_price.append((i['price'], i['code']))
    #print(new_market_price)
    sql_update = ""
    sql_update += "update tradeApp_comp set d_1price = ?, u_date = (select datetime('now', 'localtime', '" + d_day + "')) where code = ?"
    # print(sql_update)
    cur.executemany(sql_update, new_market_price)
    con.commit()
    #query_txt = " select strftime('%Y-%m-%d', time1), sum(tquan), sum(price * tquan),"
    query_txt = " select (select strftime('%Y-%m-%d', 'now', 'localtime', '" + d_day + "')), ifnull(sum(tquan),0), ifnull(sum(price * tquan),0),"
    query_txt += " round(CAST((select sum(vol * d_1price) from tradeApp_comp) AS FLOAT) / 4537700000000 * 100, 2)"
    query_txt += " from tradeApp_order"
    query_txt += " where tradeyn = 'Y'"
    query_txt += " and strftime('%Y-%m-%d', time1) = (select strftime('%Y-%m-%d', 'now', 'localtime', '" + d_day + "'))"
    cur.execute(query_txt)

    day, volume, trade_cost, ex_index = "", 0, 0, 0.0

    for row in cur.fetchall():
        print("###" * 100)
        print("###" * 100)
        print("row : ", row)
        day = row[0]
        volume = row[1]
        trade_cost = row[2]
        ex_index = row[3]
    sql_insert = ""
    sql_insert += "insert OR REPLACE into tradeApp_d_trade(day, volume, trade_cost, ex_index, regdate)"
    sql_insert += "values(?, ?, ?, ?, (select datetime('now', 'localtime', ?)))"
    cur.execute(sql_insert, (day, volume, trade_cost, ex_index, d_day))
    con.commit()
    con.close()
    print("#####  마감 완료  #####")

from datetime import datetime
import time

now = datetime.now()
nowTime = now.strftime('%H:%M:%S')

not_insert = True
point_time = "15:41:00"
while True:
    now2 = datetime.now()
    nowTime = now2.strftime('%H:%M:%S')
    if not_insert :

        if (nowTime > point_time):
            print("execute time : ", nowTime)
            d_day_str = '-0 day'
            market_price = query_market_price(d_day_str)  # 각 회사 현재가 가져옴
            # print("market_price : ", market_price)
            print("market_price : ", market_price)
            print("######## insert_daily_prices_closing")
            insert_daily_prices_closing(market_price, d_day_str)  # 날짜에 맞추어 회사 현재가 적용
            not_insert = False
        else:
            time_1 = datetime.strptime(point_time, "%H:%M:%S")
            time_interval = time_1 - (now2.strptime(nowTime, '%H:%M:%S'))
            print("Now time : ", nowTime, "마감까지 남은시간 : ", time_interval)
            time.sleep(5)
    else:
        time.sleep(5)

    print("Now time : ", nowTime)
    nowTime_list = nowTime.split(":")
    if(nowTime_list[1] == "40" or nowTime_list[1] == "41" ):
        if (nowTime_list[2] >= "00" and nowTime_list[2] <= "04"):
            bbs_update()
            print("#####  BBS UPDATE끝  #####")

