# story/views.py
from time import localtime
from story.models import Comment
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Story
from django.http import HttpResponse, JsonResponse
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
    system_user, created = User.objects.get_or_create(username="checkmarble")
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
            match_percentage=0
        )
        Comment.objects.create(
            user=system_user,
            team_id=team_id,
            text=f"{request.user.username}님이 스토리를 업로드했습니다."
        )

        # 스토리 업로드에 따른 유저 pos값 변화
        for member in team.members.all():
            user_profile = UserTeamProfile.objects.get(user=member, team=team)

        if user_profile.upload_img and (user_profile.pos_update_date is None or user_profile.pos_update_date != user_profile.upload_date):
            user_profile.pos += 1
            user_profile.pos_update_date = user_profile.upload_date
            user_profile.save()

        return redirect('teams:team_detail', team_id=team_id)

    return render(request, 'team_detail.html', {
        'error': 'Invalid request',
    })

from .models import Story
from django.views.decorators.csrf import csrf_exempt
import json
from teams.forms import CommentForm

def story_detail(request, team_id):
    from story.models import Comment
    story = get_object_or_404(Story, team_id=team_id)
    comments = Comment.objects.filter(story=story).order_by('-created_at')

    # HTML 폼 제출로 댓글 생성 (웹 페이지에서 직접 요청)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # 현재 로그인한 사용자
            comment.story = story
            comment.save()
            return redirect('story_detail', team_id=team_id)
    else:
        form = CommentForm()

    return render(
        request, 
        'story_detail.html', 
        {'story': story, 'comments': comments, 'form': form}
    )

def get_comments(request, team_id):
    from story.models import Comment
    comments = Comment.objects.filter(team_id=team_id).values('user__username', 'text')
    formatted_comments = []
    for comment in comments:
        # local_time = localtime(comment['created_at']).strftime('%p %I:%M').replace('AM', '오전').replace('PM', '오후')
        formatted_comments.append({
            "user__username": comment["user__username"],
            "text": comment["text"],
            # "timestamp": local_time,
        })
    return JsonResponse({"comments": formatted_comments})

@csrf_exempt
def create_comment(request, team_id):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get('text')
        
        if not text:
            return JsonResponse({'error': '댓글 내용을 입력하세요.'}, status=400)
        
        # team_id로 Team 객체 가져오기
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return JsonResponse({'error': '유효하지 않은 팀 ID입니다.'}, status=400)

        # 댓글 생성
        comment = Comment.objects.create(
            user=request.user,
            text=text,
            team=team  # team 필드에 Team 객체 저장
        )
        return JsonResponse({
            'message': '댓글이 성공적으로 등록되었습니다.',
            'username': comment.user.username,
            'text': comment.text
        })
    else:
        return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)