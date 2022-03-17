import json
import sqlite3

def query_db(query, args=(), one=False):
    con = sqlite3.connect('./db.sqlite3')
    cur = con.cursor()
    cur.execute(query, args)
    # r = []
    # for row in cur.fetchall():
    #     for i, value in enumerate(row):
    #         #print(cur.description[i][0], value)
    #         col = cur.description[i][0]
    #         r.append(dict(col = value))
    #     print("row : ", r)



    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

query_txt = "select A.code, B.name, A.price, A.quan"
query_txt += " from tradeApp_order A"
query_txt += " join tradeApp_comp B on(A.code = B.code)"
my_query = query_db(query_txt)
sTrade = json.dumps(my_query, ensure_ascii = False)
#ensure_ascii = False
#print(sTrade['code'])
#print(json.dumps(sTrade, indent=2))
print(sTrade)