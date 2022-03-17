from django.shortcuts import render, redirect
from .models          import *
import sqlite3
import requests
from bs4 import BeautifulSoup
# Create your views here.




def index(request) :
    print('##########try to move news code')
    create()
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
    create()
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