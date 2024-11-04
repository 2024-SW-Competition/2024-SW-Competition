#story/urls.py
from django.urls import path
from . import views

app_name = 'story'

urlpatterns = [
    path('upload/<int:team_id>/', views.upload_image, name='upload_image'),  # 업로드 URL 정의
    path('comments/<int:team_id>/', views.get_comments, name='get_comments'),
    path('comments/<int:team_id>/create/', views.create_comment, name='create_comment'),
]
