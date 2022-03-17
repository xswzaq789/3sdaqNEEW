from django.shortcuts import render

def index(request):
    print('>>>>web index')
    context = {'intro' : '3sdaq'}
    return render(request, 'index.html', context)