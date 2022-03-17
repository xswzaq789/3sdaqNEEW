from django.http      import JsonResponse
from django.shortcuts import render, redirect
import sqlite3
# Create your views here.
def index(request):
    print(">>>> index")

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
    market_price = query_market_price()
    #my_query = query_db(query_txt)
    #sTrade = json.dumps(my_query)
    # print(sTrade['code'])
    # print(json.dumps(sTrade, indent=2))
    #sTrade = json.dumps(my_query, ensure_ascii=False)

    context = {
        'sTrades': market_price
    }
    if(typeST == 'update'):
        return JsonResponse(market_price, safe=False)
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
    print('code : ', name, price, quan, code, gubun)
    my_query = query_sTrade_trade(name, price, quan, code, gubun)
    print(my_query)
    jsonAry = []

    for value in my_query:
        jsonAry.append({
            'success': 'YES'
        })
    print("sTrade_trade end")
    return JsonResponse(jsonAry, safe=False)


def query_db(query, args=(), one=False):
    print(">>>> query_db")
    con = sqlite3.connect('./db.sqlite3')
    cur = con.cursor()
    print("args : ", args)
    cur.execute(query, args)
    con.commit()

    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    con.close()
    return (r[0] if r else None) if one else r

def query_market_price():
    # query_txt = "select * from tradeApp_order"
    # query_txt += " where tradeyn = 'Y' and code = 1"
    # query_txt += " order by time1 desc"
    # query_txt += " limit 1"

    query_txt = "select * from "
    query_txt += " (select A.code, B.name, A.price,B.d_1price, A.quan, (A.price - B.d_1price) AS change, round(CAST((A.price - B.d_1price) AS FLOAT)/CAST(B.d_1price AS FLOAT) * 100, 2) as ch_rate"
    query_txt += " from tradeApp_order A"
    query_txt += " join tradeApp_comp B on(A.code = B.code)"
    query_txt += " where tradeyn = 'Y'"
    query_txt += " order by time1 desc)"
    query_txt += " group by code"
    return query_db(query_txt)

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
    query_txt += "     order by A.price desc)"
    query_txt += " Group by code, gubun, price"
    query_txt += " order by gubun desc, price desc"

    #print(query_txt)
    return query_db(query_txt)

def query_sTrade_trade(user_id, name, price, quan, code, gubun):

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
        print("my_query lenth : ", len(my_query))
        print("my_query  : ", my_query)
        if (len(my_query) == 0):
            print("1. 주식이 없어요..!!");
            return my_query
        if (len(my_query) > 0):
            print("quan : ", my_query[0]['quan'])
            if (quan > my_query[0]['quan']):
                print("2. 주식이 부족해요..!!");
                return my_query


    query_txt = " select A.id, A.code, B.name, A.gubun, A.price, B.d_1price, (A.quan - A.tquan) as quan, A.tquan, A.time1, A.buyer, A.seller"
    query_txt += " from tradeApp_order A"
    query_txt += " join tradeApp_comp B on(A.code = B.code)"
    query_txt += " where A.code = ?"
    query_txt += " and A.gubun = ?"
    query_txt += " and A.price = ?"
    query_txt += " and A.quan != A.tquan"
    query_txt += " order by A.time1 asc"
    print(query_txt)
    rgubun = "";
    other_id = "";
    if(gubun == 'B'):
        rgubun = 'S'

    elif(gubun == 'S'):
        rgubun = 'B'
    my_query = query_db(query_txt, (code, rgubun, price)) # 매수 매도할 select
    print("my_query lenth : ", len(my_query))
    print("my_query  : ", my_query)
    if (len(my_query) > 0):
        print("quan : ", my_query[0]['quan'])

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

    if (len(my_query) == 0):
        query_txt = ""
        if(gubun == "B"):
            query_txt += " insert into tradeApp_order(code, gubun, price, quan, tquan, buyer, tradeyn, time1)"
        else:
            query_txt += " insert into tradeApp_order(code, gubun, price, quan, tquan, seller, tradeyn, time1)"
        query_txt += " values(?,?, ?, ?, 0, ?, 'N', (select datetime('now','localtime')))"
        print("query_txt : ", query_txt)
        insert_query = query_db(query_txt, (code, gubun, price, quan, user_id))  # 매수 매도할 insert
        print("inert_query_db : ", my_query)

    else:
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
                query_txt += " time2=(select datetime('now','localtime')), tquan = ?"
                query_txt += " where id = ?"
                print("query_txt : ", query_txt)
                tmpGubun = "F"
                tmptquan = value['quan'] + value['tquan']
                update_query = query_db(query_txt, (tmpGubun, user_id, tmptquan, value['id']))  # 매수 매도할 update

                result = ballanceUpdateQuery(gubun, bal_query_txt, user_id, code, price, value['quan'])
                result = ballanceUpdateQuery(rgubun, bal_query_txt, other_id, code, price, value['quan'])


                cal_quan -= value['quan']
                print("1 quan, sum_quan , cal_quan ", quan, sum_quan , cal_quan)
                if quan == sum_quan:
                    print(">>>>>  quan == sum_quan")
                    print("2 quan, sum_quan , cal_quan ", quan, sum_quan, cal_quan)
                    break
            else:
                print("3 quan, sum_quan , cal_quan ", quan, sum_quan, cal_quan)
                temp_quan = (value['quan'] - cal_quan)
                # update cal_quan
                query_txt = " update tradeApp_order set"
                if (gubun == "B"):
                    query_txt += " buyer = ?, tradeyn = 'Y',"
                else:
                    query_txt += " seller = ?, tradeyn = 'Y',"
                query_txt += " time2=(select datetime('now','localtime')), tquan = ?"
                query_txt += " where id = ?"
                print("query_txt : ", query_txt)
                update_query = query_db(query_txt, (user_id, cal_quan, value['id']))  # 매수 매도할 insert
                result = ballanceUpdateQuery(gubun, bal_query_txt, user_id, code, price, value['quan'])
                result = ballanceUpdateQuery(rgubun, bal_query_txt, other_id, code, price, value['quan'])
                break
        # for end
        print("4 quan, sum_quan , cal_quan ", quan, sum_quan, cal_quan)
        if quan > sum_quan:
            print("5 quan, sum_quan , cal_quan ", quan, sum_quan, cal_quan)
            # insert cal_quan(남은거)
            query_txt = ""
            if (gubun == "B"):
                query_txt += " insert into tradeApp_order(code, gubun, price, quan, tquan, buyer, tradeyn, time1)"
            else:
                query_txt += " insert into tradeApp_order(code, gubun, price, quan, tquan, seller, tradeyn, time1)"
            query_txt += " values(?,?, ?, ?, 0, ?, 'N', (select datetime('now','localtime')))"
            print("query_txt : ", query_txt)
            insert_query = query_db(query_txt, (code, gubun, price, cal_quan, user_id))  # 매수 매도할 insert
            print("inert_query_db : ", my_query)

    return my_query

def ballanceUpdateQuery(gubun, bal_query_txt, user_id, code, price, value_quan):
    print("bal_query_txt : ", bal_query_txt)
    bal_query = query_db(bal_query_txt, (user_id, code))  # 매수 매도할 select
    print("*" * 50)
    print("*" * 50)
    print(bal_query_txt)
    print("len(bal_query) == 0 : ", len(bal_query) == 0);
    print("*" * 50)
    print("*" * 50)

    if (len(bal_query) == 0):  # Ballance 없으면 팔지못하니 insert
        print("인서트문")
        #insert문
        query_txt = " insert into tradeApp_ballance(user_id, code, price, quan, t_price, time)"
        query_txt += " values(?, ?, ?, ?, ?, (select datetime('now', 'localtime')))"
        tmp_t_price = price * value_quan
        print("tmp_t_price " , tmp_t_price)
        insert_query = query_db(query_txt, (user_id, code, price, value_quan,tmp_t_price))  # 매수 매도할 update
    else: #Ballance 있으면 update
        print("발란쓰가 있어..!!")
        if (gubun == "B"):  # 사겠다.
            tmp_t_price = price * value_quan + bal_query[0]['t_price']
            tmp_quan = bal_query[0]['quan'] + value_quan
            tmp_price = tmp_t_price//tmp_quan

            query_txt = " update tradeApp_ballance set"
            query_txt += " price =?, quan =?, t_price =?, time =(select datetime('now', 'localtime'))"
            query_txt += " where user_id =? and code=?"
            update_query = query_db(query_txt, (tmp_price, tmp_quan, tmp_t_price, user_id, code))  # 매수 매도할 update
        else: # 팔겠다.
            tmp_t_price = bal_query[0]['t_price'] - (price * value_quan)
            tmp_quan = bal_query[0]['quan'] - value_quan
            tmp_price = 0
            if(tmp_quan != 0):
                tmp_price = tmp_t_price // tmp_quan
            if(tmp_quan > 0): #물량이 있으면
                query_txt = " update tradeApp_ballance set"
                query_txt += " price =?, quan =?, t_price =?, time =(select datetime('now', 'localtime'))"
                query_txt += " where user_id =? and code=? and id=?"
                update_query = query_db(query_txt, (tmp_price, tmp_quan, tmp_t_price, user_id, code, bal_query[0]['id']))  # 매수 매도할 update
            else: #물량이 없으면
                query_txt = " delete from tradeApp_ballance"
                query_txt += " where user_id =? and code =? and id =?"
                delete_query = query_db(query_txt, (user_id, code, bal_query[0]['id']))  # 매수 매도할 update
    return 1

#query_sTrade_trade(user_id, name, price, quan, code, gubun)
#query_sTrade_trade("minsu2", "하이닉스", 100000, 30, 2, "S")
#query_sTrade_trade("minsu", "하이닉스", 100000, 70, 2, "S")
#query_sTrade_trade("minsu2", "하이닉스", 100000, 70, 2, "B")
'''
query_sTrade_trade("user4", "삼성전자", 75000, 10, 1, "S")
query_sTrade_trade("user4", "삼성전자", 76000, 20, 1, "S")
query_sTrade_trade("user6", "삼성전자", 77000, 20, 1, "S")
query_sTrade_trade("user6", "삼성전자", 78000, 30, 1, "S")
query_sTrade_trade("user6", "삼성전자", 79000, 40, 1, "S")
'''
#query_sTrade_trade("user2", "삼성전자", 78000, 20, 1, "B")
#query_sTrade_trade("user2", "삼성전자", 79000, 40, 1, "B")
#query_sTrade_trade("user2", "삼성전자", 77000, 10, 1, "B")
query_sTrade_trade("user2", "삼성전자", 76000, 10, 1, "B")
