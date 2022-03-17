from django.http      import JsonResponse
from django.shortcuts import render, redirect
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dbURL = os.path.join(BASE_DIR , 'db.sqlite3')
print("dbURL : " , dbURL)

import sqlite3
# Create your views here.
def index(request):
    print(">>>> index ")

    # if request.session.get('user_id') and request.session.get('user_name'):
    #     context = {
    #         'id' : request.session['user_id'],
    #         'name' : request.session['user_name']
    #     }
    #     return render(request, 'home.html', context)
    # else:
    #     return render(request, 'login.html')
    pass

def sTrade_list(request):
    print(">>>> sTrade_list")
    typeST = request.POST.get('typeST', '')
    user_id = request.POST.get('user_id', '')

    user_id = request.session['user_id']
    print("user_id : ", user_id)
    d_day = '-0 day'
    market_price = query_market_price(d_day)
    myStock_price = query_myStock_price(user_id)
    #my_query = query_db(query_txt)
    #sTrade = json.dumps(my_query)
    # print(sTrade['code'])
    # print(json.dumps(sTrade, indent=2))
    #sTrade = json.dumps(my_query, ensure_ascii=False)
    for value in market_price:
        value['price'] = getComma(value['price'])
        value['d_1price'] = getComma(value['d_1price'])
        value['sum_tquan'] = getComma(value['sum_tquan'])
        value['change'] = getComma(value['change'])
        value['ch_rate'] = str(value['ch_rate']) + "%"
    for value in myStock_price:
        value['d_1price'] = getComma(value['d_1price'])
        value['price'] = getComma(value['price'])
        value['change'] = getComma(value['change'])
        value['myprice'] = getComma(value['myprice'])
        value['quan'] = getComma(value['quan'])
        value['income_rate'] = str(value['income_rate']) + "%"
        value['t_price'] = getComma(value['t_price'])

    context = {
        'sTrades': market_price,
        'myTrades' : myStock_price
    }
    if(typeST == 'update'):
        return JsonResponse(context, safe=False)
    else:
        return render(request, 'sTrade/sTrade_list.html', context)

def detail_order(request):
    print(">>>> detail_order")
    code = request.POST['code']
    #print('code : ', code)
    my_query = query_detail_order(code)
    #print(my_query)
    jsonAry = []

    for value in my_query:
        jsonAry.append({
            'code': value['code'],
            'name': value['name'],
            'gubun': value['gubun'],
            'price': value['price'],
            'quan': value['quan']
        })
    return JsonResponse(jsonAry, safe=False)

def sTrade_trade(request):
    print(">>>> sTrade_trade")

    name = request.POST.get('name', '')
    price = int(request.POST.get('price', ''))
    quan = int(request.POST.get('quan', ''))
    code = int(request.POST.get('code', ''))
    gubun = request.POST.get('gubun', '')
    #print('code : ', name, price, quan, code, gubun)
    user_id = request.session['user_id']
    d_day = '-0 day'
    my_query = query_sTrade_trade(user_id, price, quan, code, gubun, d_day)
    #print(my_query)
    #print(my_query == [])
    jsonAry = []
    for value in my_query:
        if(my_query != []):
            try:
                print(value['error'])
                print("value['error'] : ", value['error'])
                response = JsonResponse({"error": value['error']})
                response.status_code = 403  # To announce that the user isn't allowed to publish

                return response
            except:
                print("##########################################except!!!!")
                print("except!!!!")
                return JsonResponse(jsonAry, safe=False)

    return JsonResponse(jsonAry, safe=False)
    #my_query = [{"error": "주식이 부족해요..!!"}]
    #return sTrade_list(request)


def query_db(query, args=(), one=False):
    #print(">>>> query_db")
    con = sqlite3.connect(dbURL)
    cur = con.cursor()
    #print("args : ", args)
    cur.execute(query, args)
    con.commit()

    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    con.close()
    return (r[0] if r else None) if one else r

def query_market_price(d_day):
    # query_txt = "select * from tradeApp_order"
    # query_txt += " where tradeyn = 'Y' and code = 1"
    # query_txt += " order by time1 desc"
    # query_txt += " limit 1"

    # query_txt = "select * from "
    # query_txt += " (select A.code, B.name, A.price,B.d_1price, A.quan, (A.price - B.d_1price) AS change, round(CAST((A.price - B.d_1price) AS FLOAT)/CAST(B.d_1price AS FLOAT) * 100, 2) as ch_rate"
    # query_txt += " from tradeApp_order A"
    # query_txt += " join tradeApp_comp B on(A.code = B.code)"
    # query_txt += " where tradeyn = 'Y'"
    # query_txt += " order by time2 desc)"
    # query_txt += " group by code"

    # query_txt = "select * from "
    # query_txt += " (select A.code, A.name, ifnull(B.price,A.d_1price) as price , A.d_1price, (ifnull(B.price,A.d_1price) - A.d_1price) AS change, round(CAST((ifnull(B.price,A.d_1price) - A.d_1price) AS FLOAT)/CAST(A.d_1price AS FLOAT) * 100, 2) as ch_rate"
    # query_txt += " from tradeApp_comp  A"
    # query_txt += " left join tradeApp_order B on(A.code = B.code and B.time2 > (select strftime('%Y-%m-%d', 'now', 'localtime', '"+d_day+"')))"
    # query_txt += " where 1 = 1"
    # query_txt += " order by B.time2 desc)"
    # query_txt += " group by code"

    query_txt = " select * from"
    query_txt += " (  select A.code, A.name, ifnull(B.price,A.d_1price) as price , A.d_1price, (ifnull(B.price,A.d_1price) - A.d_1price) AS change,"
    query_txt += "           round(CAST((ifnull(B.price,A.d_1price) - A.d_1price) AS FLOAT)/CAST(A.d_1price AS FLOAT) * 100, 2) as ch_rate, sum_tquan"
    query_txt += "    from tradeApp_comp  A"
    query_txt += "    left join (select * , sum(tquan) as sum_tquan"
    query_txt += "          from (select * from tradeApp_order where tradeyn = 'Y' and time2 > (select strftime('%Y-%m-%d', 'now', 'localtime', '"+d_day+"')) order by time2 desc)"
    query_txt += "          group by code) B"
    query_txt += "    on (A.code = B.code)"
    query_txt += " )"
    query_txt += " order by code"
    print("query_txt : ", query_txt)
    return query_db(query_txt)

def query_myStock_price(user_id):

    query_txt = " select D.*, (D.esti_price - D.t_price) as income"
    query_txt += " from( select A.code, B.name, ifnull(C.price, B.d_1price) as price, B.d_1price, (ifnull(C.price, B.d_1price) - B.d_1price) AS change, A.price as myprice, A.quan,"
    query_txt += " round(CAST((ifnull(C.price, B.d_1price) - A.price) AS FLOAT)/CAST(A.price AS FLOAT) * 100, 2) as income_rate, A.t_price, (A.quan * ifnull(C.price, B.d_1price)) AS esti_price"
    query_txt += " from tradeApp_ballance A"
    query_txt += " join tradeApp_comp B on (A.code = B.code)"
    query_txt += " left join tradeApp_order C on(A.code = C.code and C.time2 > (select strftime('%Y-%m-%d', 'now', 'localtime')))"
    query_txt += " where 1 = 1"
    query_txt += " and A.user_id = ?"
    query_txt += " order by C.time2 desc)D"
    query_txt += " group by code"
    #print("query_txt,  " , query_txt)
    return query_db(query_txt, (user_id,))



def query_detail_order(code):
    # query_txt = "select * from tradeApp_order"
    # query_txt += " where tradeyn = 'Y' and code = 1"
    # query_txt += " order by time1 desc"
    # query_txt += " limit 1"


    # query_txt = " select A.code, B.name, A.gubun, A.price, B.d_1price, (A.quan - A.tquan) as quan"
    # query_txt += " from tradeApp_order A"
    # query_txt += " join tradeApp_comp B on(A.code = B.code)"
    # query_txt += " where A.quan != A.tquan"
    # query_txt += " and A.code = "+code
    # query_txt += " order by A.price desc"

    query_txt = " select code, name, gubun, price, d_1price, sum(quan) as quan"
    query_txt += " from (select A.code, B.name, A.gubun, A.price, B.d_1price, (A.quan - A.tquan) as quan"
    query_txt += "    from tradeApp_order A"
    query_txt += "     join tradeApp_comp B on(A.code = B.code)"
    query_txt += "     where A.code =" + code
    query_txt += "     and A.gubun != 'C'"
    query_txt += "     and A.quan != A.tquan"
    query_txt += "     and A.time1 > (select strftime('%Y-%m-%d', 'now', 'localtime'))"
    query_txt += "     order by A.price desc)"
    query_txt += " Group by code, gubun, price"
    query_txt += " order by gubun desc, price desc"

    #print(query_txt)
    return query_db(query_txt)

def query_sTrade_trade(user_id, price, quan, code, gubun, d_day):

    #print("query_sTrade_trade user_id, price : ",user_id, " : " , price)
    bal_query_txt = ""
    bal_query_txt = " select A.id, A.user_id, A.code, A.price, A.quan, A.t_price"
    bal_query_txt += " from tradeApp_ballance A"
    bal_query_txt += " where A.user_id = ?"
    bal_query_txt += " and A.code = ?"
    if(gubun == 'S'):
        # query_txt = " select A.user_id, A.code, B.name, A.price, A.quan, A.t_price"
        # query_txt += " from tradeApp_ballance A"
        # query_txt += " join tradeApp_comp B on(A.code = B.code)"
        # query_txt += " where A.user_id = ?"
        # query_txt += " and A.code = ?"
        # query_txt += " order by A.code asc"


        my_query = query_db(bal_query_txt, (user_id, code))  # 매수 매도할 select
        #print("my_query lenth : ", len(my_query))
        #print("my_query  : ", my_query)
        #print("###############11111111################")
        if (len(my_query) == 0):
            #print("###############122222222################")
            print("1. 주식이 없어요..!!");
            my_query = [{"error":"주식이 없어요"}]
            return my_query
        if (len(my_query) > 0):
            #print("###############33333333################")
            #print("quan : ", my_query[0]['quan'])

            query_txt = " select ifnull(sum(B.quan - B.tquan),0) as sum_quan from tradeApp_comp  A"
            query_txt += " left join tradeApp_order B on(A.code = B.code and B.time1 > (select strftime('%Y-%m-%d', 'now', 'localtime', '"+d_day+"')))"
            query_txt += " where B.seller = ? and B.gubun = ? and B.code = ?"
            ch_sell_quan = query_db(query_txt, (user_id, gubun, code))  # 매수 매도할 select
            sum_quan = quan + ch_sell_quan[0]['sum_quan']
            #print("quan,ch_sell_quan[0]['sum_quan'],my_query[0]['quan']   ",quan,ch_sell_quan[0]['sum_quan'],my_query[0]['quan'])
            if (sum_quan > my_query[0]['quan']):
                #print("###############444444444################")
                #print("2. 주식이 부족해요..!!");
                my_query = [{"error": "주식이 부족해요..!!"}]
                return my_query

    rgubun = "";
    other_id = "";
    if (gubun == 'B'):
        rgubun = 'S'

    elif (gubun == 'S'):
        rgubun = 'B'
    query_txt = " select A.id, A.code, B.name, A.gubun, A.price, B.d_1price, (A.quan - A.tquan) as quan, A.tquan, A.time1, A.buyer, A.seller"
    query_txt += " from tradeApp_order A"
    query_txt += " join tradeApp_comp B on(A.code = B.code)"
    query_txt += " where A.code = ?"
    query_txt += " and A.gubun = ?"
    if (rgubun == 'B'):
        query_txt += " and A.price >= ?"
    else:
        query_txt += " and A.price <= ?"
    query_txt += " and A.quan != A.tquan"
    query_txt += " and A.time1 > (select strftime('%Y-%m-%d', 'now', 'localtime', '"+d_day+"'))"
    if (rgubun == 'B'):
        query_txt += " order by A.price desc, A.time1 asc"
    else:
        query_txt += " order by A.price asc, A.time1 asc"
    #print(query_txt)

    my_query = query_db(query_txt, (code, rgubun, price)) # 매수 매도할 select
    #print("my_query lenth : ", len(my_query))
    #print("my_query  : ", my_query)
    #if (len(my_query) > 0):
        #print("quan : ", my_query[0]['quan'])

    # if len(my_query) == 0
    #     insert 매수
    # else:
    #     quan을 합할 변수지정
    #     for in select
    #         sum 변수에 합하고
    #         if 매수quan이 <= sum
    #             update F
    #         else:
    #             B - A 만큼만 update 상태는 B,S
    #             break;


    sum_quan = 0
    cal_quan = quan
    for value in my_query:
        sum_quan += value['quan']
        if (gubun == 'B'):
            other_id = value['seller']
        elif (gubun == 'S'):
            other_id = value['buyer']
        if cal_quan >= value['quan']:
            query_txt = " update tradeApp_order set"
            if (gubun == "B"):
                query_txt += " gubun = ?, buyer = ?, tradeyn = 'Y',"
            else:
                query_txt += " gubun = ?, seller = ?, tradeyn = 'Y',"
            query_txt += " time2=(select datetime('now','localtime', '"+d_day+"')), tquan = ?"
            query_txt += " where id = ?"
            #print("query_txt : ", query_txt)
            tmpGubun = "F"
            tmptquan = value['quan'] + value['tquan']
            update_query = query_db(query_txt, (tmpGubun, user_id, tmptquan, value['id']))  # 매수 매도할 update
            #print("value['quan'] :::: ", value['quan'])
            result = ballanceUpdateQuery(gubun, bal_query_txt, user_id, code, value['price'], value['quan'], d_day)
            result = ballanceUpdateQuery(rgubun, bal_query_txt, other_id, code, value['price'], value['quan'], d_day)


            cal_quan -= value['quan']
            #print("1 quan, sum_quan , cal_quan ", quan, sum_quan , cal_quan)
            if quan == sum_quan:
                #print(">>>>>  quan == sum_quan")
                #print("2 quan, sum_quan , cal_quan ", quan, sum_quan, cal_quan)
                break
        else:
            #print("3 quan, sum_quan , cal_quan ", quan, sum_quan, cal_quan)
            temp_quan = (value['tquan'] + cal_quan)
            # update cal_quan
            query_txt = " update tradeApp_order set"
            if (gubun == "B"):
                query_txt += " buyer = ?, tradeyn = 'Y',"
            else:
                query_txt += " seller = ?, tradeyn = 'Y',"
            query_txt += " time2=(select datetime('now','localtime', '"+d_day+"')), tquan = ?"
            query_txt += " where id = ?"
            #print("query_txt : ", query_txt)
            update_query = query_db(query_txt, (user_id, temp_quan, value['id']))  # 매수 매도할 insert
            #print("value['quan'] :::: " , value['quan'])
            result = ballanceUpdateQuery(gubun, bal_query_txt, user_id, code, value['price'], cal_quan, d_day)
            result = ballanceUpdateQuery(rgubun, bal_query_txt, other_id, code, value['price'], cal_quan, d_day)
            break
    # for end
    #print("4 quan, sum_quan , cal_quan ", quan, sum_quan, cal_quan)
    if quan > sum_quan:
        #print("5 quan, sum_quan , cal_quan ", quan, sum_quan, cal_quan)
        # insert cal_quan(남은거)
        query_txt = ""
        if (gubun == "B"):
            query_txt += " insert into tradeApp_order(code, gubun, price, quan, tquan, buyer, tradeyn, time1)"
        else:
            query_txt += " insert into tradeApp_order(code, gubun, price, quan, tquan, seller, tradeyn, time1)"
        query_txt += " values(?,?, ?, ?, 0, ?, 'N', (select datetime('now','localtime', '"+d_day+"')))"
        #print("query_txt : ", query_txt)
        insert_query = query_db(query_txt, (code, gubun, price, cal_quan, user_id))  # 매수 매도할 insert
        #print("inert_query_db : ", my_query)

    return my_query

def ballanceUpdateQuery(gubun, bal_query_txt, user_id, code, price, value_quan, d_day):
    #print("bal_query_txt : ", bal_query_txt)
    bal_query = query_db(bal_query_txt, (user_id, code))  # 매수 매도할 select
    #print("*" * 50)
    #print("*" * 50)
    #print(bal_query_txt)
    #print("len(bal_query) == 0 : ", len(bal_query) == 0);
    #print("*" * 50)
    #print("*" * 50)

    sql_select = "select user_amt from userApp_webuser where user_id = ?"
    amt_query = query_db(sql_select, (user_id,))
    user_amt = amt_query[0]['user_amt']

    if (len(bal_query) == 0):  # Ballance 없으면 팔지못하니 insert
        #print("인서트문")
        #insert문
        query_txt = " insert into tradeApp_ballance(user_id, code, price, quan, t_price, time)"
        query_txt += " values(?, ?, ?, ?, ?, (select datetime('now', 'localtime', '"+d_day+"')))"
        tmp_t_price = price * value_quan
        #print("tmp_t_price " , tmp_t_price)
        insert_query = query_db(query_txt, (user_id, code, price, value_quan,tmp_t_price))  # 매수 매도할 update
        user_amt -= tmp_t_price
        query_txt = " update userApp_webuser set user_amt = ? where user_id = ? "
        user_amt_query = query_db(query_txt, (user_amt, user_id))  # 유저의 현금을 차감
    else: #Ballance 있으면 update
        #print("발란쓰가 있어..!!")
        if (gubun == "B"):  # 사겠다.
            tmp_t_price = price * value_quan + bal_query[0]['t_price']
            tmp_quan = bal_query[0]['quan'] + value_quan
            #print("tmp_quan, bal_query[0]['quan'], value_quan, price", tmp_quan, bal_query[0]['quan'], value_quan, price)
            tmp_price = tmp_t_price//tmp_quan

            query_txt = " update tradeApp_ballance set"
            query_txt += " price =?, quan =?, t_price =?, time =(select datetime('now', 'localtime', '"+d_day+"'))"
            query_txt += " where user_id =? and code=?"
            update_query = query_db(query_txt, (tmp_price, tmp_quan, tmp_t_price, user_id, code))  # 매수 매도할 update
            #print("query_txt ::", query_txt)
            user_amt -= price * value_quan
            query_txt = " update userApp_webuser set user_amt = ? where user_id = ? "
            user_amt_query = query_db(query_txt, (user_amt, user_id))  # 유저의 현금을 차감
        else: # 팔겠다.
            #tmp_t_price = bal_query[0]['t_price'] - (price * value_quan) # 기존코드 : 현재가에서뺀다
            tmp_t_price = bal_query[0]['t_price'] - (bal_query[0]['price'] * value_quan) # 팔때는 현재가가아닌 기존의 매입가에서 빼줘야한다. 
            tmp_quan = bal_query[0]['quan'] - value_quan
            tmp_price = 0
            if(tmp_quan != 0):
                tmp_price = tmp_t_price // tmp_quan
            if(tmp_quan > 0): #물량이 있으면
                query_txt = " update tradeApp_ballance set"
                query_txt += " price =?, quan =?, t_price =?, time =(select datetime('now', 'localtime', '"+d_day+"'))"
                query_txt += " where user_id =? and code=? and id=?"
                update_query = query_db(query_txt, (tmp_price, tmp_quan, tmp_t_price, user_id, code, bal_query[0]['id']))  # 매수 매도할 update
                #print("query_txt ::", query_txt)
            else: #물량이 없으면
                query_txt = " delete from tradeApp_ballance"
                query_txt += " where user_id =? and code =? and id =?"
                delete_query = query_db(query_txt, (user_id, code, bal_query[0]['id']))  # 매수 매도할 update
            user_amt += price * value_quan
            query_txt = " update userApp_webuser set user_amt = ? where user_id = ? "
            user_amt_query = query_db(query_txt, (user_amt, user_id))  # 유저의 현금을 가산
    return 1

def auto_sTrade_trade(user_id, price, quan, code, gubun):
    print("#" * 100)
    print("#" * 100)
    print(">>>>>>>  auto_sTrade_trade - Start")

    print("user_id : ", user_id)
    print("price : ", price)
    print("quan : ", quan)
    print("code : ", code)
    print("gubun : ", gubun)

    print(">>>>>>>  auto_sTrade_trade - End")

    print("#" * 100)
    print("#" * 100)

def auto_sTrade_trade_print():

    print("auto_sTrade_trade_print!!")

def getComma(value):
    str_value = str(value)
    new_value = ""
    for i, v in enumerate(range(len(str_value), 0,-1)):
        if(i%3 == 0 and i != 0):
            new_value = "," + new_value
        new_value = str_value[v-1] + new_value
    return new_value
#  2022-03-13 00:07


def sTrade_charts(request):
    print(">>>> sTrade_charts")
    typeST = request.POST.get('typeST', '')
    user_id = request.POST.get('user_id', '')

    user_id = request.session['user_id']
    d_day = '-0 day'
    market_price = query_market_price(d_day)
    for value in market_price:
        value['price'] = getComma(value['price'])
        value['d_1price'] = getComma(value['d_1price'])
        value['change'] = getComma(value['change'])
        value['ch_rate'] = str(value['ch_rate']) + "%"
    print("market_price : ", market_price)
    context = {
        'sTrades': market_price,
    }
    if(typeST == 'update'):
        return JsonResponse(context, safe=False)
    else:
        return render(request, 'sTrade/charts.html', context)

def sTrade_code_data(request):
    print(">>>> sTrade_code_data")
    code = request.POST.get('code', '')
    print("trCode : ", code);
    #query_txt = " select *, max(price) as max_price, min(price) as min_price from tradeApp_d_price where code = ?"
    query_txt = " select A.*, (max_price * 1.000) as max_price, (min_price * 1.000) as min_price "
    query_txt += " from tradeApp_d_price A"
    query_txt += " left join (select code, max(price) as max_price from tradeApp_d_price where code = ? and day > (select strftime('%Y-%m-%d', 'now', 'localtime', '-14 day'))) B"
    query_txt += " left join (select code, min(price) as min_price from tradeApp_d_price where code = ? and day > (select strftime('%Y-%m-%d', 'now', 'localtime', '-14 day'))) C"
    query_txt += " on A.code = B.code "
    query_txt += " and A.code = C.code"
    query_txt += " where A.code = ?"
    query_txt += " and A.day > (select strftime('%Y-%m-%d', 'now', 'localtime', '-14 day'))"

    sTrade_code_data_query = query_db(query_txt, (code, code, code))  # 종목조회 select
    print("sTrade_code_data_query : ", sTrade_code_data_query)
    day_list = []
    price_list = []
    max_price = []
    min_price = []
    name = []
    for value in sTrade_code_data_query:
        day_list.append(value['day'])
        price_list.append(value['price'])
        max_price.append(value['max_price'])
        min_price.append(value['min_price'])
        name.append(value['name'])
    print("day_list : ", day_list)
    jsonAry = []
    print("max_price[0] : ", max_price[0]);
    jsonAry.append({
        'day_list': day_list,
        'price_list': price_list,
        'max_price': max_price[0],
        'min_price': min_price[0],
        'name': name[0],
    })
    print(jsonAry)
    return JsonResponse(jsonAry, safe=False)

def sTrade_myAccount(request) :
    print(">>>> sTrade_myAccount")
    typeST = request.POST.get('typeST', '')
    user_id = request.POST.get('user_id', '')

    user_id = request.session['user_id']
    query_txt = " select user_amt from userApp_webuser where user_id = ?"
    sTrade_amt_query = query_db(query_txt, (user_id, ))  # 현금조회 select
    print("## : ", sTrade_amt_query)
    print("### : ", sTrade_amt_query[0]['user_amt'])
    
    
    d_day = '-0 day'
    stock_prices = 0
    myStock_price = query_myStock_price(user_id)


    for value in myStock_price:

        value['d_1price'] = getComma(value['d_1price'])
        value['price'] = getComma(value['price'])
        value['change'] = getComma(value['change'])
        value['myprice'] = getComma(value['myprice'])
        value['quan'] = getComma(value['quan'])
        value['income_rate'] = str(value['income_rate']) + "%"

        stock_prices += value['esti_price']
        print("stock_prices : ", value['t_price'])
        print("stock_prices : ", stock_prices)
        value['t_price'] = getComma(value['t_price'])
        value['esti_price'] = getComma(value['esti_price'])
    user_amt = int(sTrade_amt_query[0]['user_amt'])
    tot_asset = stock_prices + user_amt
    print("stock_prices : ", stock_prices)
    print("user_amt : ", user_amt)
    print("tot_asset : ", tot_asset)

    context = {
        'myTrades': myStock_price,
        'user_amt': getComma(user_amt),
        'tot_asset': getComma(tot_asset),
        'stock_prices': getComma(stock_prices),
    }

    if (typeST == 'update'):
        return JsonResponse(context, safe=False)
    else:
        return render(request, 'sTrade/myAccount.html', context)














