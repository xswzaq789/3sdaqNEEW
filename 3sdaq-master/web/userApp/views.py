from django.shortcuts import render , redirect
from .models          import *
import time
import os.path
import sqlite3
import requests
from bs4 import BeautifulSoup

# Create your views here.
def index(request) :
    print(">>>>> user index")
    if request.session.get('user_name') :
        print('>>>> login session exits!!')
        context = {
            'session_user_name' : request.session['user_name'] ,
            'session_user_id': request.session['user_id'],
        }
        return redirect('../../bbs/index')
        #return render(request, 'user/ok.html' , context)
    else :
        return render(request , 'user/index.html')

# select * from WebUser where user_id = x and user_pwd = x
# orm : modelName.objects.get()
# select * from WebUser
# orm : modelName.objects.all()
# session tracking m
def login(request) :
    print('>>>> user login')
    if request.method == 'POST' :
        print('>>>> request post')
        id  = request.POST['id']
        pwd = request.POST['pwd']
        print('>>>> request param - ', id, pwd)

        # model - DB(Select)
        # 정보를 담는 작업을 필요로 한다.
        context = {}
        try :
            user = WebUser.objects.get(user_id = id , user_pwd = pwd)
            # 세션을 만드는 과정
            request.session['user_name'] = user.user_name
            request.session['user_id'] = user.user_id
            request.session['user_pwd'] = user.user_pwd
            # 세션을 심는 과정
            context['session_user_name'] = request.session['user_name']
            context['session_user_id'] = request.session['user_id']
            context['session_user_pwd'] = request.session['user_pwd']
            return redirect('../../bbs/index', context)
            #return render(request, 'user/ok.html', context)
        except Exception as e:
            context['error'] = 'invalid id, pwd'
            return render(request , 'user/index.html' , context)


def registerForm(request):
    print('>>>> user registerForm - ')
    return render(request , 'user/join.html')

def join(request) :
    print('>>>> user join - ')
    id   = request.POST['id']
    pwd  = request.POST['pwd']
    name = request.POST['name']
    print('>>>> param values - ', id, pwd, name)
    # insert into table(id, pwd, name) values('','','')
    # orm : modelName(attr - value).save()
    WebUser(user_id = id , user_pwd = pwd , user_name = name).save()
    # return render(request , 'user/index.html')
    return redirect('main')

def aboutUs(request):
    return render(request, 'user/aboutUs.html')

def aboutUs2(request):
    try:
        session_user_id = request.session['user_id']
        return render(request, 'user/aboutUs2.html')
    except Exception as e:
        print("e : ", e)
        return redirect('main')

def mypage(request):
    print(">>>>> user page")
    try:
        session_user_id = request.session['user_id']
        if request.session.get('user_name'):
            print('>>>> Yeah!!')
            context = {
                'session_user_name': request.session['user_name'],
                'session_user_id': request.session['user_id'],
                'session_user_pwd' : request.session['user_pwd'],
            }
        return render(request, 'user/mypage.html', context)
    except Exception as e:
        print("e : ", e)
        return redirect('main')

def logout(request) :
    print(">>>> user logout")
    # 세션을 삭제
    request.session['user_name'] = {}
    request.session['user_id'] = {}
    request.session['user_pwd'] = {}
    request.session.modified = True

    # 새로운 request url을 정의할 때
    return redirect('main')

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



# def update():
#     response = requests.get("https://finance.naver.com/news/mainnews.naver")
#
#     html = response.text
#
#     soup = BeautifulSoup(html, 'html.parser')
#     links = soup.select(".articleSubject")
#
#     fdic = {}
#     title = []
#     url = []
#
#     for link in links:
#         x = 'http://finance.naver.com' + link.find('a')['href'].strip()
#         url.append(x)
#
#         y = link.text.strip()
#         title.append(y)
#
#     for i in range(len(links)):
#         fdic[i] = [title[i], url[i]]
#
#     print(fdic)
#     #
#     conn = sqlite3.connect("../db.sqlite3")
#     cur = conn.cursor()
#
#
#     conn.execute("drop table news")
#     conn.execute("create table news(id integer, title text, url text)")
#
#     for i in fdic:
#         title = fdic[i][0]
#         url = fdic[i][1]
#         sql = "insert into news values(?,?,?)"
#         cur.execute(sql,(i,title,url))
#
#     conn.commit()
#     conn.close()

