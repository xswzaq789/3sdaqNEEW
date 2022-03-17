from django.shortcuts import render, redirect
from .models          import *
import sqlite3
import requests
from bs4 import BeautifulSoup
# Create your views here.

from django.http      import JsonResponse
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dbURL = os.path.join(BASE_DIR , 'db.sqlite3')






def index(request) :
    print('##########try to move news code')
    #create()
    users = BbsUser.objects.all()
    news = SBS.objects.all()
    for n in news:
        print(n.url)
    context = {'users': users,
               'news': news}
    return render(request, 'index2.html', context)

def login(request) :
    return render(request, 'login2.html')

def logout(request) :
    print(">>>> user logout")
    # 세션을 삭제
    request.session['user_name'] = {}
    request.session['user_id'] = {}
    request.session.modified = True

    # 새로운 request url을 정의할 때
    return redirect('main')

# 여기에서 sqlite 값 가져오면 될듯? ?
def charts(request) :
    installation = [3068, 2970, 2839, 2977, 2663 , 2665 ]
    context = {
        'installation' : installation
    }
    return render(request,  'charts.html', context)

def news(request):
    print('##########try to move news code')
    #create()
    users = BbsUser.objects.all()
    news = SBS.objects.all()
    for n in news:
        print(n.url)
    context = {'users': users,
               'news': news}
    return 0

def create():
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
    #
    conn = sqlite3.connect("./db.sqlite3")
    cur = conn.cursor()


    conn.execute("drop table if exists userApp_sbs")
    conn.execute("create table userApp_sbs(id integer, title text, url text)")

    for i in fdic:
        title = fdic[i][0]
        url = fdic[i][1]
        sql = "insert into userApp_sbs values(?,?,?)"
        cur.execute(sql, (i+1, title, url))
    conn.commit()
    conn.close()

def myLineChart(request) :
    print(">>>>> myLineChart")

    con = sqlite3.connect(dbURL)
    cur = con.cursor()
    query_txt = " select day, ex_index from tradeApp_d_trade where day > (select strftime('%Y-%m-%d', 'now', 'localtime', '-14 day'))"
    cur.execute(query_txt)
    labels = []
    ex_index = []
    min_value = 0
    max_value = 0
    for row in cur.fetchall():
        labels.append(row[0])
        ex_index.append(row[1])
        if(min_value > row[1] or min_value == 0):
            min_value = row[1]
        if (max_value < row[1]):
            max_value = row[1]
    print("labels : ", labels)
    print("ex_index : ", ex_index)
    cur.connection.close()
    con.close()

    jsonAry = []
    my_query = []
    #my_query = [{"id":3000}]
    #for value in my_query:
    jsonAry.append({
        'labels' : labels,
        'ex_index': ex_index,
        'min_value': min_value,
        'max_value': max_value,
    })
    print(jsonAry)
    return JsonResponse(jsonAry, safe=False)