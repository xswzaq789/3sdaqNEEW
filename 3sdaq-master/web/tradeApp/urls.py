from django.contrib import admin
from django.urls import path, include
from tradeApp import views
print("tradeApp urls")
urlpatterns = [
    # http://127.0.0.1:8000/trade/index
    path('index/', views.index, name='index'),
    path('', views.sTrade_list),
    path('sTrade_list/', views.sTrade_list, name='sTrade_list'),
    path('detail_order/', views.detail_order, name='detail_order'),
    path('sTrade_trade/', views.sTrade_trade, name='sTrade_trade'),
    path('sTrade_charts/', views.sTrade_charts, name='sTrade_charts'),
    path('sTrade_code_data/', views.sTrade_code_data, name='sTrade_code_data'),
    path('sTrade_myAccount/', views.sTrade_myAccount, name='sTrade_myAccount'),

]
