# story/models.py
from django.db import models
from django.contrib.auth.models import User
from home.models import Home
from teams.models import Team
from teams.models import UserTeamProfile
from django.contrib import admin

class Story(models.Model):
    # story_id = models.PublicKey 
    # story_id는 장고에서 자동으로 기본 키 생성해줌
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 부모 객체가 삭제될 때 자식도 같이 삭제됨
    expire_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    upload_image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    match_percentage = models.IntegerField(null=True, blank=True)   # ai가 분석한 목표와 스토리 일치율
    

    # 캐릭터. 외래키
    character_image = models.ForeignKey(UserTeamProfile, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return f"Story by {self.user.username}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)  # Team 모델과의 관계 설정

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"
