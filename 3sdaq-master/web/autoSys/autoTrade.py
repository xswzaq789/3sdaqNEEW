import os
import random
import sys
import sqlite3
from random import sample, randrange
from math import floor
from datetime import datetime
'''
보현 주석 테스트############
'''
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

from views import query_sTrade_trade

'''
    가격 선택
'''
def price_list(now_price, b_or_s):
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

    if(b_or_s == "B") :
        select_price = random.choices(price_list, weights=[1, 2, 10, 12, 10, 2, 1], k=1)
        return select_price[0]
    if (b_or_s == "S"):
        select_price = random.choices(price_list, weights=[1, 2, 10, 12, 10, 2, 1], k=1)
        return select_price[0]

cur = con.cursor()

b_or_s_list = ["B","S","B","S","B","S","S","S","B","S","B","S"]
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

    sql_select = "select user_id from userApp_webuser"
    cur.execute(sql_select)

    for row in cur.fetchall():
        user_list.append(row[0])


'''
    AUTO트레이딩
'''
def stock_auto_trade():
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
        if(user_id == "blackrock"): #시장지배자 
            continue
        #b_or_s = random.choice(b_or_s_list)
        b_or_s_list2 = sample(b_or_s_list, k=1)
        b_or_s = b_or_s_list2[0][0]
        #b_or_s_list = random.choices(b_or_s_list, weights=[1, 1], k=1)
        #b_or_s = b_or_s_list[0]

        # 회사선택
        if(b_or_s == "B"): 
            print("len(comp_list) ", len(comp_list))
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
        query_txt += " left join tradeApp_order B on(A.code = B.code and B.time1 > (select strftime('%Y-%m-%d', 'now', 'localtime'))"
        query_txt += "    and B.quan = B.tquan and B.tradeyn='Y')"
        query_txt += " where A.code = ?"
        query_txt += " order by B.time2 desc"

        #print("query_txt,  ", query_txt)
        cur.execute(query_txt, (code,))
        now_price = 0
        for row in cur.fetchall():
            now_price = row[2]
        #print("now_price : ", now_price)

        price = price_list(now_price, b_or_s) # 가격 결정
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
            select_quan = randrange(10, 100, 10)  # 수량 결정
        #print('user_id, price, select_quan, code, b_or_s : ', user_id, price, select_quan, code, b_or_s)
        d_day = '-0 day'
        query_sTrade_trade(user_id, price, select_quan, code, b_or_s, d_day)
        #print("countB, countS, total1 : ", countB, countS, countB+countS)
    # 15초와 45초일때 5분지난(거래가 되지않은 order)삭제
    now = datetime.now()
    nowTime = now.strftime('%S')
    if (nowTime == "15" or nowTime == "45"):
        delete_not_sold()

def delete_not_sold():
    import datetime

    dt_now = datetime.datetime.now()
    #d_today = datetime.date.today()
    # datetime.datetime.now() - datetime.timedelta(minutes=15)
    stand_time = (dt_now - datetime.timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')
    query_txt = " delete from tradeApp_order where tradeyn = 'N' and time1 < ?"
    #print("###############################")
    #print("##########  delete 시작 ########")
    cur.execute(query_txt, (stand_time,))
    con.commit()
    #print("##########  delete 끝 ##########")
    #print("###############################")



list_setting() #유저세팅
while_count = 0
while True :
    if(True):
        stock_auto_trade() # 트레이딩
    #  2022-03-13 00:07














