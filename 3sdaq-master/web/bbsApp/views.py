from django.shortcuts import render, redirect

# Create your views here.




def index(request) :
   return render(request, 'index2.html')

def login(request) :
    return render(request, 'login2.html')

def detail(request):
    print('>>>> user detail')
    id = request.GET['id']
    print('>>>> param id - ' , id)
    user = WebUser.objects.get(user_id = id)
    if user is not None :
        context = {'user' : user}
    else :
        context = {'error': '사용자 정보가 존재하지 않습니다!!'}

    return render(request , 'user/detail.html' , context)

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

