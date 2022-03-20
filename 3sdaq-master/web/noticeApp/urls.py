from django.urls    import path , include
from noticeApp        import views

urlpatterns = [
    # http://127.0.0.1:8000/notice/index
    path('index/',              views.index ,       name='notice_index'),
    path('createForm/',         views.createForm ,  name='notice_createForm'),
    path('notice_create/',      views.create ,      name='notice_create'),
    path('notice_read/',        views.read ,        name='notice_read'),
    path('notice_remove/',      views.remove ,      name='notice_remove'),
    path('notice_update/',      views.update ,      name='notice_update'),
    path('notice_search/',      views.search,       name='notice_search'),
]
