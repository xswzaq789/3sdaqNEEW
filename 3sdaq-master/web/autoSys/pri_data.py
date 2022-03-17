import sqlite3
from random import sample, randrange
con = sqlite3.connect('../db.sqlite3')

def input_webuser():
    cur = con.cursor()
    count = 1
    while True:

        sql_insert = ""
        sql_insert += "insert into userApp_webuser(user_id, user_pwd, user_name, user_acct, user_amt, user_regdate)"
        sql_insert += "values('user" + str(count) + "', 'user" + str(count) + "', '유저" + str(count) + "', '001-23456-0" + str(count) + "' ,1000000000, (select datetime('now', 'localtime')))"
        #print(sql_insert)
        cur.execute(sql_insert)
        count += 1
        if(count > 20):
            sql_insert = ""
            sql_insert += "insert into userApp_webuser(user_id, user_pwd, user_name, user_acct, user_amt, user_regdate)"
            sql_insert += "values('blackrock', 'blackrock', 'blackrock', '999-23456-651' ,1000000000000000, (select datetime('now', 'localtime')))"
            # print(sql_insert)
            cur.execute(sql_insert)
            break
    con.commit()
    print("input_webuser 완료")
    #end input_webuser()

def input_comp():
    cur = con.cursor()

    sql_insert = ""
    sql_insert += "insert into tradeApp_comp(code, name, type, vol, d_1price, regdate)"
    sql_insert += "values(?,?,?,?,?,(select datetime('now', 'localtime')))"
    comp_list = [
        (1, '삼성전자', 'IT', 1000000, 71500),
        (2, 'LG에너지솔루션', '화학', 1000000, 428500),
        (3, 'SK하이닉스', 'IT', 1000000, 124500),
        (4, 'NAVER', 'IT', 1000000, 317500),
        (5, '삼성바이오로직스', '제약', 1000000,775000),
        (6, '카카오', 'IT', 1000000, 94700),
        (7, 'LG화학', '화학', 1000000, 535000),
        (8, '현대차', '자동차', 1000000, 172500),
        (9, '삼성SDI', 'IT', 1000000, 528000),
        (10, '기아', '자동차', 1000000, 73100),
        (11, 'POSCO', '철강', 1000000, 291500),
        (12, 'KB금융', '금융', 1000000, 57500),
        (13, '카카오뱅크', '금융', 1000000, 48700),
        (14, '셀트리온', '제약', 1000000, 167000),
        (15, '현대모비스', '자동차', 1000000, 225000),
        (16, '삼성물산', '물류', 1000000, 110500),
        (17, 'LG전자', 'IT', 1000000, 123500),
        (18, '신한지주', '금융', 1000000, 38200),
        (19, 'SK이노베이션', '화학', 1000000, 212000),
        (20, '카카오페이', '금융', 1000000, 143500),
    ]

    #print(sql_insert)
    cur.executemany(sql_insert, comp_list)
    con.commit()
    print("input_comp 완료")
    #end input_comp()

def input_ballance():
    cur = con.cursor()
    sql_select = "select user_id from userApp_webuser"
    #print(sql_select)
    cur.execute(sql_select)
    user_list = []
    for row in cur.fetchall():
        user_list.append(row[0])
    sql_select = "select code, d_1price from tradeApp_comp"
    #print(sql_select)
    cur.execute(sql_select)
    comp_list = []
    for row in cur.fetchall():
        comp_list.append([row[0], row[1]])

    for user_id in user_list:
        if (user_id == "blackrock"):
            buy_list = sample(comp_list, k=20)
        else:
            buy_list = sample(comp_list, k=5)
        #print(buy_list)
        for code, d_1price in buy_list:
            #print(code, d_1price)


            if(user_id == "blackrock"):
                quan = randrange(1000, 50000, 1000)
            else:
                quan = randrange(100, 300, 10)
            t_price = d_1price * quan

            sql_select = "select user_amt from userApp_webuser where user_id = ?"
            cur.execute(sql_select, (user_id,))

            amt = 0
            for amtV in cur.fetchall():
                amt = amtV[0]

            amt -= t_price
            if(amt < 0):
                break
            sql_update = ""
            sql_update += "update userApp_webuser set user_amt = ? where user_id = ?"
            cur.execute(sql_update, (amt, user_id))


            sql_insert = ""
            sql_insert += "insert into tradeApp_ballance(user_id, price, quan, t_price, code, time)"
            sql_insert += "values(?,?,?,?,?,(select datetime('now', 'localtime')))"
            cur.execute(sql_insert, (user_id, d_1price, quan, t_price, code))



    con.commit()
    print("input_ballance 완료")
    #end input_ballance()

def clear_inputData():
    cur = con.cursor()
    sql_delete = "delete from userApp_webuser"
    cur.execute(sql_delete)
    sql_delete = "delete from tradeApp_ballance"
    cur.execute(sql_delete)
    sql_delete = "delete from tradeApp_comp"
    cur.execute(sql_delete)
    sql_delete = "delete from tradeApp_order"
    cur.execute(sql_delete)
    sql_delete = "delete from tradeApp_d_price"
    cur.execute(sql_delete)
    sql_delete = "delete from tradeApp_d_trade"
    cur.execute(sql_delete)
    sql_update = "update sqlite_sequence set seq = 0 where name = 'tradeApp_ballance'"
    cur.execute(sql_update)
    sql_update = "update sqlite_sequence set seq = 0 where name = 'userApp_webuser'"
    cur.execute(sql_update)
    sql_update = "update sqlite_sequence set seq = 0 where name = 'tradeApp_order'"
    cur.execute(sql_update)
    sql_update = "update sqlite_sequence set seq = 0 where name = 'tradeApp_d_price'"
    cur.execute(sql_update)
    sql_update = "update sqlite_sequence set seq = 0 where name = 'tradeApp_d_trade'"
    cur.execute(sql_update)
    con.commit()
    print("clear_inputData 완료 ")
    # end clear_inputData()

clear_inputData()
input_webuser()
input_comp()
input_ballance()

con.close()

#  2022-03-13 00:07





