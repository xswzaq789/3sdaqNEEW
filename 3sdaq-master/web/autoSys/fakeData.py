import os
import random
import sys
import sqlite3
from random import sample, randrange
from math import floor
from datetime import datetime

'''
    FakeData는 시장지배자를 참여시켜 등락폭을 높이고
    데일리 저장시킴
'''

'''
 sqlite 위치 
'''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print("BASE_DIR : ", BASE_DIR)
dbURL = os.path.join(BASE_DIR , 'db.sqlite3')
#print("dbURL : ", dbURL)
tradeAppURL = os.path.join(BASE_DIR , 'tradeApp')
#print("tradeAppURL : " , tradeAppURL)
sys.path.append(tradeAppURL)
#print(BASE_DIR)
con = sqlite3.connect(dbURL)

from views import query_sTrade_trade
from views import query_market_price

'''
    가격 선택
'''
def price_list(now_price, b_or_s, d_state):
    price_list = []
    price_list.append(now_price)
    temp_price = now_price
    count = 1
    while count < 4 :  #시세에 따라 등락폭 조정
        count +=1
        if (temp_price <= 1000):
            temp_price -= 1
        elif (temp_price <= 5000):
            temp_price -= 5
        elif (temp_price <= 10000):
            temp_price -= 10
        elif (temp_price <= 50000):
            temp_price -= 50
        elif (temp_price <= 100000):
            temp_price -= 100
        elif (temp_price <= 500000):
            temp_price -= 500
        else :
            temp_price -= 5000
        price_list.append(temp_price)
    count = 1
    temp_price = now_price
    while count < 4:
        count += 1
        if (temp_price < 1000):
            temp_price += 1
        elif (temp_price < 5000):
            temp_price += 5
        elif (temp_price < 10000):
            temp_price += 10
        elif (temp_price < 50000):
            temp_price += 50
        elif (temp_price < 100000):
            temp_price += 100
        elif (temp_price < 500000):
            temp_price += 500
        else:
            temp_price += 5000
        price_list.append(temp_price)
    price_list.sort()
    #print("b_or_s, d_state : ", b_or_s, d_state)
    if(b_or_s == "B" and d_state == "GOOD") :
        select_price = random.choices(price_list, weights=[0, 0, 2, 5, 12, 8, 2], k=1)
        return select_price[0]
    if (b_or_s == "B" and d_state == "SOSO"):
        select_price = random.choices(price_list, weights=[1, 2, 10, 12, 10, 2, 1], k=1)
        return select_price[0]
    elif (b_or_s == "B" and d_state == "BAD"):
        select_price = random.choices(price_list, weights=[2, 8, 12, 5, 2, 0, 0], k=1)
        return select_price[0]
    elif (b_or_s == "S" and d_state == "GOOD"):
        select_price = random.choices(price_list, weights=[0, 0, 2, 5, 12, 8, 2], k=1)
        return select_price[0]
    elif (b_or_s == "S" and d_state == "SOSO"):
        select_price = random.choices(price_list, weights=[1, 2, 10, 12, 10, 2, 1], k=1)
        return select_price[0]
    elif (b_or_s == "S" and d_state == "BAD"):
        select_price = random.choices(price_list, weights=[2, 8, 12, 5, 2, 0, 0], k=1)
        return select_price[0]
cur = con.cursor()

b_or_s_list = ["B","S","B","S","B","S","B","S","B","S","B","S"]
user_list = []
comp_list = []
countB = 0
countS = 0

'''
    유저세팅
'''
def list_setting():
    global user_list
    global comp_list

    sql_select = "select user_id from userApp_webuser where user_name like '%_Bot'"
    cur.execute(sql_select)

    for row in cur.fetchall():
        user_list.append(row[0])


'''
    AUTO트레이딩
'''
def stock_auto_trade(d_state, d_day):
    ######################
    ######################
    ## K 값 조정하세요..!! ##
    ######################
    ######################
    global countB
    global countS
    global comp_list
    global b_or_s_list
    global user_list
    #트레이드할 유저선택
    trade_user_list = sample(user_list, k=1)

    sql_select = "select code from tradeApp_comp"
    cur.execute(sql_select)
    for row in cur.fetchall():
        comp_list.append([row[0]])

    for user_id in trade_user_list:
        #if(user_id == "blackrock"): #시장지배자
        #    continue
        #b_or_s = random.choice(b_or_s_list)
        b_or_s_list2 = sample(b_or_s_list, k=1)
        b_or_s = b_or_s_list2[0][0]
        #b_or_s_list = random.choices(b_or_s_list, weights=[1, 1], k=1)
        #b_or_s = b_or_s_list[0]

        # 회사선택
        if(b_or_s == "B"): 
            #("len(comp_list) ", len(comp_list))
            selected_comp = sample(comp_list, k=1)
            countB += 1
        else : # sell일때 회사선택
            countS += 1
            comp_list = []
            sql_select = "select code from tradeApp_ballance where user_id = ?"
            cur.execute(sql_select, (user_id,) )
            for row in cur.fetchall():
                comp_list.append([row[0]])

            #print("len(comp_list) == 0 ", (len(comp_list) == 0))
            if(len(comp_list) == 0):
                continue
            selected_comp = sample(comp_list, k=1)

        #print("selected_comp : ", selected_comp[0][0])
        code = selected_comp[0][0]


        query_txt = " select A.code, A.d_1price, ifnull(B.price, A.d_1price) as price"
        query_txt += " from tradeApp_comp A"
        query_txt += " left join tradeApp_order B on(A.code = B.code and B.time1 > (select strftime('%Y-%m-%d', 'now', 'localtime', '"+d_day+"'))"
        query_txt += "    and B.quan = B.tquan and B.tradeyn='Y')"
        query_txt += " where A.code = ?"
        query_txt += " order by B.time2 desc"

        #print("query_txt,  ", query_txt)
        cur.execute(query_txt, (code,))
        now_price = 0
        for row in cur.fetchall():
            now_price = row[2]
        #print("now_price : ", now_price)

        price = price_list(now_price, b_or_s, d_state) # 가격 결정
        #print("now_price2 : ", price)
        select_quan = 0
        if (b_or_s == "S"):
            query_txt = " select quan from tradeApp_ballance where user_id = ? and code = ?"
            cur.execute(query_txt, (user_id, code))
            have_quan = 0
            for row in cur.fetchall():
                have_quan = row[0]
            #print("have_quan : ", have_quan)
            if (have_quan <= 50): # 100 주 아래로 가지고있으면 전량 판매
                select_quan = have_quan
                #print("1 have_quan , ", have_quan)
            elif(have_quan > 300):
                have_quan = int(floor((have_quan/2)/10) * 10)
                #print("2 have_quan , ", have_quan)
                select_quan = randrange(50, have_quan, 10)  # 수량 결정
            else:
                #print("3 have_quan , ", have_quan)
                select_quan = randrange(50, have_quan, 10)  # 수량 결정
        else:
            if(user_id == "blackrock"): #시장지배자
                if (d_state == "GOOD"):
                    select_quan = randrange(100, 2000, 100)  # 수량 결정
                if (d_state == "SOSO"):
                    select_quan = randrange(100, 700, 100)  # 수량 결정
                if (d_state == "BAD"):
                    select_quan = randrange(100, 300, 100)  # 수량 결정
            else:
                select_quan = randrange(10, 100, 10)  # 수량 결정
        #print('user_id, price, select_quan, code, b_or_s : ', user_id, price, select_quan, code, b_or_s)
        query_sTrade_trade(user_id, price, select_quan, code, b_or_s, d_day)
        #print("countB, countS, total1 : ", countB, countS, countB+countS)

'''
    거래가 없었던 데이터 지움
'''
def delete_not_sold(d_day):
    query_txt = " delete from tradeApp_order where tradeyn = 'N' and time1 <= (select strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime', '"+d_day+"'))"
    #print("###############################")
    #print("##########  delete 시작 ########")
    #print("query_txt :  ", query_txt)
    cur.execute(query_txt)
    con.commit()
    #print("##########  delete 끝 ##########")
    #print("###############################")

'''
    현재가 저장
'''
def insert_daily_prices(market_price, d_day):
    #print("############   insert_daily_prices  ###################")
    new_market_price_insert = []
    new_market_price_update = []
    for i in market_price:
        query_txt = " select EXISTS( select * from tradeApp_d_price where day = strftime('%Y-%m-%d', 'now', 'localtime', ?) and code = ?)"
        exist_day_code = 0
        cur.execute(query_txt, (d_day, i['code']))
        for row in cur.fetchall():
            #print("###" * 100)
            #print("###" * 100)
            #print("row : ", row)
            exist_day_code = row[0]
        if (exist_day_code == 1):
            #print("update")
            new_market_price_update.append((i['price'], i['code']))
        else:
            #print("insert")
            new_market_price_insert.append((i['code'], i['name'], i['price']))
        # new_market_price.append((i['code'], i['name'], i['price']))
    # print(new_market_price)
    sql_insert = ""
    sql_insert += "insert into tradeApp_d_price(day, code, name, price, regdate)"
    sql_insert += "values((select strftime('%Y-%m-%d', 'now', 'localtime', '" + d_day + "')), ?, ?, ?, (select datetime('now', 'localtime', '" + d_day + "')))"
    #print(sql_insert)
    #print(new_market_price_insert)
    cur.executemany(sql_insert, new_market_price_insert)
    con.commit()
    sql_update = ""
    sql_update += "update tradeApp_d_price set price = ?, regdate = (select datetime('now', 'localtime', '" + d_day + "'))"
    sql_update += "where day = (select strftime('%Y-%m-%d', 'now', 'localtime', '" + d_day + "')) and code = ?"
    #print(sql_update)
    #print(new_market_price_update)
    cur.executemany(sql_update, new_market_price_update)
    con.commit()
    new_market_price = []
    for i in market_price:
        new_market_price.append((i['price'], i['code']))
    #print(new_market_price)
    sql_update = ""
    sql_update += "update tradeApp_comp set d_1price = ?, u_date = (select datetime('now', 'localtime', '" + d_day + "')) where code = ?"
    # print(sql_update)
    cur.executemany(sql_update, new_market_price)
    con.commit()

    query_txt = " select (select strftime('%Y-%m-%d', 'now', 'localtime', '" + d_day + "')), ifnull(sum(tquan),0), ifnull(sum(price * tquan),0),"
    query_txt += " round(CAST((select sum(vol * d_1price) from tradeApp_comp) AS FLOAT) / 4537700000000 * 100, 2)"
    query_txt += " from tradeApp_order"
    query_txt += " where tradeyn = 'Y'"
    query_txt += " and strftime('%Y-%m-%d', time1) = (select strftime('%Y-%m-%d', 'now', 'localtime', '" + d_day + "'))"
    cur.execute(query_txt)

    day, volume, trade_cost, ex_index = "", 0, 0, 0.0

    for row in cur.fetchall():
        #print("###" * 100)
        #print("###" * 100)
        #print("row : ", row)
        day = row[0]
        volume = row[1]
        trade_cost = row[2]
        ex_index = row[3]
    sql_insert = ""
    sql_insert += "insert OR REPLACE into tradeApp_d_trade(day, volume, trade_cost, ex_index, regdate)"
    sql_insert += "values(?, ?, ?, ?, (select datetime('now', 'localtime', ?)))"
    cur.execute(sql_insert, (day, volume, trade_cost, ex_index, d_day))
    con.commit()
    print('날짜 : ', day, ' 거래량 : ', volume, ' 거래대금 : ', trade_cost, ' 3스닥지수 : ', ex_index)


list_setting() #유저세팅
while_count = 0
#while True :
#    if(True):
#        stock_auto_trade() # 트레이딩
    #  2022-03-13 00:07

for i in range(14, -1, -1): # 2주 기준으로 현재가 설정(오늘꺼까지 총 15일)

    d_day_str = '-' + str(i) + ' day'
    print("Day : ", d_day_str + " 데이터 생성중...")
    d_state = random.choices(['GOOD', 'SOSO', 'BAD'], weights=[6, 3, 2], k=1) # 그날의 상태 적용
    #print("day, state : ", d_day_str, d_state[0])
    import datetime
    dt_now = datetime.datetime.now()
    stand_time = (dt_now + datetime.timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
    #stand_time = (dt_now + datetime.timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')
    stand_time = datetime.datetime.strptime(stand_time, '%Y-%m-%d %H:%M:%S')
    while True :
        if(True):
            stock_auto_trade(d_state[0], d_day_str) # 트레이딩
            dt_now2 = datetime.datetime.now()
            if(dt_now2 > stand_time): # 지정된 시간이 되면 break
                break

    delete_not_sold(d_day_str) # 거래가 되지않은 데이터 지우고
    market_price = query_market_price(d_day_str) # 각 회사 현재가 가져옴
    #print("market_price : ", market_price)
    #print("insert_daily_prices 호출")
    insert_daily_prices(market_price, d_day_str) # 날짜에 맞추어 회사 현재가 적용
print("## fakeData 완료 ##")
con.close()








