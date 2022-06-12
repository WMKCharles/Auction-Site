from unicodedata import name
from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('create/', views.create_auction, name='create'),
    path('active/', views.active, name='active'),
    # path('active/<str:category_name>', views.active, name='active'),

    path('watchlist/', views.watchlist, name='watchlist'),
    path('watchlist/<int:auction_id>/edit/<str:reverse_method>/', views.watchlist_edit, name='watchlist_edit'),
    path('auction/<str:auction_id>', views.auction_detail, name='auction_detail'),

    #bid url

    path('auction/<str:auction_id>/bid', views.bid, name='bid'),
    path('auction/<str:auction_id>/close/', views.auction_close, name='auction_close'),

    #comment url 
    path('auction/<str:auction_id>/comment/', views.comment, name='auction_comment'),

    # Product categories url 
    path('categories/<str:category_name>', views.category_detail, name='category_detail'),
]