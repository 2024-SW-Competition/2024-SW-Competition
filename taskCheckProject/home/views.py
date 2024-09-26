# home > views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from teams.models import UserTeamProfile, Team
from .models import Home
from story.models import Story


# team 정보에 맞춰 home 업데이트
def update_home(request, team_id):
  team=get_object_or_404(Team, id=team_id)
  home = get_object_or_404(Home, team=team)

  if request.method == 'POST':
      # n일차 계산
    today = timezone.now().date()
    delta = (today - home.start_date.date()).days   #오늘날짜-시작일 차이
    home.date = delta + 1  # 1일차부터 시작해서 +1
    home.save()
  
    return redirect('teams:team_detail', team_id=team_id)
      
  return render(request, 'team_detail.html', {
     'team': team,
     'home': home
     })



# 보드게임판 칸 리스트 생성
def board_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    home = get_object_or_404(Home, team=team)
    duration = team.duration
    users = team.members.all()

    # 행 개수 계산 (5일당 2줄)
    rows = (duration // 5) * 2 + (1 if duration % 5 > 0 else 0)
    columns = 4
    # 게임판 모양 2차원 배열 초기화
    board = [[-1 for _ in range(columns)] for _ in range(rows)]

    # s자 모양으로 1 배치
    count = 0
    for row in range(rows):
        if count >= duration:  # duration 초과 시 종료
            break
        
        if row % 4 == 0:  # 0, 4, 8 ... 번째 행 (왼쪽에서 오른쪽)
            for col in range(columns):
                if count < duration:
                    board[row][col] = count
                    count += 1
        elif row % 4 == 1:  # 1, 5 ... 번째 행 (첫 번째 열에 값)
            board[row][columns - 1] = count
            count += 1
        elif row % 4 == 2:  # 2, 6 ... 번째 행 (오른쪽에서 왼쪽)
            for col in range(columns - 1, -1, -1):
                if count < duration:
                    board[row][col] = count
                    count += 1
        elif row % 4 == 3:  # 3, 7 ... 번째 행 (마지막 열에 값)
            board[row][0] = count
            count += 1

    flipped_board = board[::-1]  # 배열을 뒤집기

    team_members_profiles = get_team_members_profiles(request, team_id)

    return render(request, 'team_detail.html', {
        'rows': range(rows),
        'columns': range(columns),
        'duration': duration,
        'team': team,
        'board': flipped_board,
        'team_members_profiles':team_members_profiles,
    })


def get_team_members_profiles(request, team_id):
   team = get_object_or_404(Team, id=team_id)
   team_members_profiles = []
   for member in team.members.all():
        try:
            user_profile = UserTeamProfile.objects.get(user=member, team=team)
            team_members_profiles.append({
                'member': member,
                'character_image': user_profile.character_image,
                'pos': user_profile.pos  # 위치도 함께 저장
            })
        except UserTeamProfile.DoesNotExist:
            team_members_profiles.append({
                'member': member,
                'character_image': None,
                'pos': 0  # 기본값 설정
            })
   return team_members_profiles


  

# 보드게임판 위 유저 위치 설정 -> 위에 포함시켜야
def user_pos(request, home_id):
  home = get_object_or_404(Home, id=home_id)

  if request.method == 'POST':
      users = UserTeamProfile.objects.filter(team=home.team)    # 팀에 속한 사용자만 선택

      for user in users:
        # story가 활성화 되면 한칸 이동
        active_story = Story.objects.filter(user=user, is_active=True).first()
    
        if active_story:    
          current_pos = user.pos
          user.pos = current_pos + 1    # 위치 업데이트
          user.save()
      
      home.save()

  team_id = home.team.id
  return redirect('home:board_view', team_id=team_id)