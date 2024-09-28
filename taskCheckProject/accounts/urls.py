from django.urls import path
from accounts import views

app_name = "accounts" 

urlpatterns = [
    # 회원가입
    path('join/', views.join, name='join'),

    # 로그인/로그아웃
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # 회원가입 성공
    path('start/', views.start, name='start'),

    # 홈화면
    path('home/', views.home, name='home'),
]