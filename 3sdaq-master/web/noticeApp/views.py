from django.http      import JsonResponse
from django.shortcuts import render , redirect
from .models          import *
# Create your views here.
def index(request) :
    print('>>>>> notice index')
    # model - orm : modelName.objects.all()
    boards = WebNotice.objects.all().order_by('-id')
    print('notice result type  - ' , type(boards))
    print('notice result value - ' , boards)
    context = {
        'boards' : boards
    }

    return render(request , 'notice/index.html' , context)

def createForm(request) :
    print(">>>> notice form")
    return render(request, 'notice/createForm.html')

def create(request) :
    print(">>>> notice create")
    title   = request.POST['title']
    writer  = request.POST['writer']
    content = request.POST['content']
    print('debuge - ', title, writer, content)

    # orm - insert - save()
    notice = WebNotice(title=title , writer = writer , content = content)
    notice.save()

    return redirect('notice_index')

def read(request) :
    print('>>>> notice read')
    id = request.GET['id']
    print('debuge - ' , id)
    # select
    board = WebNotice.objects.get(id = id)
    # update - commit - save()
    board.viewcnt = board.viewcnt + 1
    board.save()

    context = {
        'board' : board
    }
    return render(request , 'notice/read.html' , context)

def remove(request) :
    print(">>>> notice remove")
    id = request.GET['id']
    print(">>>> debuge - " , id)
    # orm - delete
    board = WebNotice.objects.get(id=id)
    board.delete()

    return redirect('notice_index')

def update(request) :
    print('>>>> bss update ')
    title   = request.GET['title']
    id      = request.GET['id']
    content = request.GET['content']
    print('debuge - ', title, id , content)
    # orm - update
    board = WebNotice.objects.get(id=id)
    board.title   = title
    board.content = content
    board.save() # commit

    return redirect('notice_index')

def search(request):
    print('>>>>> notice search')
    type = request.POST['type']
    keyword = request.POST['keyword']
    print('debug', type, keyword)
    jsonAry = [
        {'id': 'pbh', 'title': '공지'},
        {'id': 'admin', 'title': '즐거운 금요일'},
    ]
    return JsonResponse(jsonAry, safe = False)

