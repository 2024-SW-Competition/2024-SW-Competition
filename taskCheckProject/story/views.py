# story/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Story
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from teams.models import Team, UserTeamProfile
from django.utils import timezone
from datetime import datetime
import pytz # pip install pytz
from django.urls import reverse
from datetime import timedelta

@login_required(login_url='accounts:login')
def team_detail_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    upload_url = reverse('story:upload_image', kwargs={'team_id': team_id})  # URL 생성 테스트
    print(f"Generated upload URL: {upload_url}")  # 디버깅용으로 URL을 출력합니다.
    
    userProfiles = UserTeamProfile.objects.filter(team=team)

    return render(request, 'teams:team_detail.html', {
        'team': team,
        'team_id': team_id,
        'upload_url': upload_url,  # 디버깅용으로 URL을 템플릿에 전달
        'team_members_profiles':userProfiles,
    })


def story_view(request, team_id):
    if not request.user.is_authenticated:
        user = User.objects.filter(username='admin').first()  
    else: 
        user = request.user

    # team_id로 팀을 가져옴
    team = get_object_or_404(Team, id=team_id)

    # UserTeamProfile 조회 또는 생성
    user_profile, created = UserTeamProfile.objects.get_or_create(user=user, team=team)

    # KST 기준으로 현재 날짜를 가져오기
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.now(kst).date()

     # 업로드 이미지가 오늘 업로드된 것인지 확인
    is_today = False
    if user_profile.upload_date:
        upload_date = user_profile.upload_date.date()
        is_today = (upload_date == today)
    
    # 캐릭터 이미지 및 업로드 이미지 가져오기
    character_image = user_profile.character_image
    upload_image = user_profile.upload_img.url if user_profile.upload_img else None

    print("Character Image: {character_image}, Upload Image: {upload_image}, is_today: {is_today}")

    # 업로드 된 스토리가 현재 날짜를 지나면 None
    if user_profile.upload_date and user_profile.upload_date < today:
        upload_image = None

    # 스토리 가져오기 (최대 5개)
    # user_stories = Story.objects.filter(team=team).select_related('user').order_by('user')[:5]

    return render(request, 'team_detail.html', {
        'character': character_image,
        'upload_img': upload_image,
        # 'user_stories': user_stories,
        'team_id': team_id,
        'today': today,
        'is_today': is_today,
    })

def upload_image(request, team_id):
    if request.method == 'POST' and 'img' in request.FILES:
        team = get_object_or_404(Team, id=team_id)
        user_profile, created = UserTeamProfile.objects.get_or_create(user=request.user, team=team)

        user_profile.upload_img = request.FILES['img']
        user_profile.upload_date = timezone.now()
        user_profile.save()

        print(f"Upload Image: {user_profile.upload_img}")

        # 오늘 자정으로 만료 시간 설정
        kst = pytz.timezone('Asia/Seoul')  # 한국 표준시
        now = timezone.now().astimezone(kst)
        today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)  # 오늘 자정

        # 스토리 자동 생성
        Story.objects.create(
            user=request.user,
            team=team,
            upload_image=user_profile.upload_img,  # UserTeamProfile을 통해 업로드 이미지 참조
            character_image=user_profile,  # UserTeamProfile을 통해 캐릭터 이미지 참조
            expire_time=today_midnight,  # 오늘 자정에 만료되도록 설정
            #is_today=True  # 업로드된 당일의 스토리로 표시
        )

        team_members_profiles = UserTeamProfile.objects.filter(team=team)

        return redirect('teams:team_detail', team_id=team_id)

    return render(request, 'team_detail.html', {
        'error': 'Invalid request',
    })