from unicodedata import name
from django.urls import path 

from . import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('active/', views.active, name='active'),
    path('create/', views.create_auction, name='create'),
    path('watch/', views.watch, name='watch'),
    # path('login/', views.login, name ='login'),
]