#story/urls.py
from django.urls import path
from . import views

app_name = 'story'

urlpatterns = [
    path('upload/<int:team_id>', views.upload_image, name='upload_image'),  # 업로드 URL 정의
]
