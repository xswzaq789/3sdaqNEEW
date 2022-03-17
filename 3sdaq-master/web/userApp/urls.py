from django.urls    import path , include
from userApp        import views

urlpatterns = [
    # http://127.0.0.1:8000/user/login
    path('index/',          views.index , name='index'),
    path('login/',          views.login),
    #path('list/' ,          views.list),
   # path('detail/' ,        views.detail),
    path('registerForm/' ,  views.registerForm),
    path('join/' ,          views.join),
    path('logout/' ,          views.logout),
    path('aboutUs/',        views.aboutUs),
    path('aboutUs2/',        views.aboutUs2),
    path('mypage/',         views.mypage),
]



