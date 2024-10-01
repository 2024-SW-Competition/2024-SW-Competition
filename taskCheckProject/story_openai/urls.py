#story_openai/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('story_query', views.query_view, name='story_query_view'),
]
