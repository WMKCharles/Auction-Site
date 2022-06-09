from unicodedata import name
from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('active/', views.active, name='active'),
    path('create/', views.create_auction, name='create'),
    path('watch/', views.watch, name='watch'),
    # path('login/', views.login, name ='login'),
]