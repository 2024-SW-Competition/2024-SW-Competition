from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# 팀 생성
class Team(models.Model):
    name = models.CharField(max_length=100)  # 팀 이름 필드
    members = models.ManyToManyField(User, related_name='teams')  # 팀 멤버들
    goal = models.CharField(max_length=255)  # 팀 목표
    duration = models.PositiveIntegerField()  # 목표 기간 (일수)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.name

# 팀별 유저프로필
class UserTeamProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    character_image = models.CharField(max_length=100)  # 사용자가 선택한 캐릭터 이미지
    upload_img = models.ImageField(upload_to='uploads/', null=True, blank=True)  # 업로드이미지
    expire_date = models.DateTimeField(null=True, blank=True)
    upload_date = models.DateField(default=timezone.now, null=True, blank=True) # 업로드한 날짜를 기록하기 위함

    class Meta:
        unique_together = ('user', 'team')  # 같은 팀에서 같은 사용자가 중복된 프로필을 갖지 않도록

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"
    
    def save(self, *args, **kwargs):
        if self.upload_date:
            # 현재 날짜의 자정을 expire_date로 설정
            self.expire_date = datetime.combine(self.upload_date, datetime.min.time()) + timedelta(days=1)
        super().save(*args, **kwargs)

# 초대하기
class Invite(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    code = models.CharField(max_length=4, unique=True)
    # invited_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return self.code

