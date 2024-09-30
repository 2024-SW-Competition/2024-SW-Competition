#home/urls.py
from django.urls import path
from home import views 
app_name = 'home'

urlpatterns = [
    # path('team_board/<int:team_id>/', views.board_view, name='team_board'),

    path('completion/<int:team_id>/', views.completion, name='completion'),
]