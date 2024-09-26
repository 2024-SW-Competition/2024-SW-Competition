#home/urls.py
from django.urls import path
from home import views 
app_name = 'home'

urlpatterns = [
    #path('update/<int:team_id>/', views.update_home, name='update_home'),

    path('boardView/<int:team_id>/', views.board_view, name='board_view'),

    #path('teams/team-detail/<int:team_id>/', views.user_pos, name='user_pos'),
]