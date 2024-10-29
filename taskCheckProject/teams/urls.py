#teams/urls.py
from django.urls import path
from teams import views

app_name = "teams"

urlpatterns = [
    # 팀 조인
    path('join-team/', views.join_team, name='join_team'),

    # 팀 생성
    path('create-team/', views.create_team, name='create_team'),

    # 캐릭터 선택
    path('choose-character/<int:team_id>/', views.choose_character, name='choose_character'),

    # 팀 상세페이지
    path('team-detail/<int:team_id>/', views.team_detail, name='team_detail'),

   # openAI 코멘트
   path('get_comment/', views.get_openai_comment_view, name='get_openai_comment'),
]

