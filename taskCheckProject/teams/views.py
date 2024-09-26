from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Invite, Team, UserTeamProfile
from .forms import CreateTeamForm, JoinTeamForm
import random
import string
from home.models import Home
from home.views import update_home
from django.utils import timezone


# 초대코드 생성
def generate_invite_code():
    return ''.join(random.choices(string.digits, k=4))


# 팀 생성
def create_team(request):
    if request.method == 'POST':
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            goal = form.cleaned_data['goal']
            duration = form.cleaned_data['duration']

            # 초대 코드 생성 및 저장
            invite_code = generate_invite_code()

            # 팀 생성
            team = Team.objects.create(
                name=name,
                goal=goal,
                duration=duration,
                code=invite_code,
            )


            users = UserTeamProfile.objects.filter(team=team)
            # 홈 생성
            Home.objects.create(
                team=team,
                goal=team.goal,
                start_date=timezone.now(),
                date=1,
                is_end=False,
                invitation_num=team.code,
                )

            Invite.objects.create(code=invite_code, team=team)

            print(f'팀 "{name}"이(가) 생성되었습니다. 초대 코드는 {invite_code}입니다.')
            messages.success(request, f'팀 "{name}"이(가) 생성되었습니다. 초대 코드는 {invite_code}입니다.')
            return redirect('teams:choose_character', team_id=team.id)
        else:
            print(form.errors)  # 유효성 검사 오류 출력
    else:
        form = CreateTeamForm()
    
    return render(request, 'create_team.html', {'form': form})


# 팀 조인
def join_team(request):
    if request.method == 'POST':
        form = JoinTeamForm(request.POST)
        if form.is_valid():
            invite_code = form.cleaned_data['invite_code']

            try:
                invite = Invite.objects.get(code=invite_code)
                team = invite.team
                user = request.user

                if user in team.members.all():
                    print('이미 팀에 가입되어 있습니다.')
                    messages.info(request, '이미 팀에 가입되어 있습니다.')
                elif team.members.count() >= 5:
                    print('이 팀은 이미 최대 인원 수에 도달했습니다.')
                    messages.error(request, '이 팀은 이미 최대 인원 수에 도달했습니다.')
                else:
                    # 팀에 가입 처리 후 캐릭터 선택 페이지로 리디렉션
                    return redirect('teams:choose_character', team_id=team.id)

            except Invite.DoesNotExist:
                print('유효하지 않은 초대 코드입니다.')
                messages.error(request, '유효하지 않은 초대 코드입니다.')
        else:
            print(form.errors)  # 유효성 검사 오류 출력

    else:
        form = JoinTeamForm()

    return render(request, 'invite.html', {'form': form})


# 캐릭터 선택 페이지
def choose_character(request, team_id):
    team = Team.objects.get(id=team_id)
    user = request.user

    # 팀원들이 이미 선택한 캐릭터 이미지 리스트를 가져옴
    chosen_characters = team.userteamprofile_set.values_list('character_image', flat=True)

    if request.method == 'POST':
        character_image = request.POST.get('character_image')
        
        # 선택한 캐릭터를 팀과 사용자에게 저장
        UserTeamProfile.objects.update_or_create(
            user=user,
            team=team,
            defaults={'character_image': character_image}
        )

        team.members.add(user)
        
        print(f'캐릭터 "{character_image}" 선택 완료.')
        messages.success(request, '캐릭터가 성공적으로 선택되었고 팀에 가입되었습니다.')

        
        # 팀 상세 페이지로 리디렉션
        return redirect('teams:team_detail', team_id=team.id)

    return render(request, 'choose_character.html', {'team_id': team_id, 'team': team, 'chosen_characters': chosen_characters})


# 팀 상세페이지
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    home = get_object_or_404(Home, team=team)

    if request.user not in team.members.all():
        messages.error(request, "이 팀에 접근할 권한이 없습니다.")
        return redirect('accounts:home')  # 권한이 없는 경우 이동할 페이지

    # 각 팀원의 UserTeamProfile 정보를 가져오기
    team_members_profiles = []
    for member in team.members.all():
        try:
            user_profile = UserTeamProfile.objects.get(user=member, team=team)
            team_members_profiles.append({
                'member': member,
                'character_image': user_profile.character_image,
                'pos': user_profile.pos
            })
        except UserTeamProfile.DoesNotExist:
            team_members_profiles.append({
                'member': member,
                'character_image': None,
                'pos': None
            })

    update_home(request, team_id)

    return render(request, 'team_detail.html', {
        'team': team,
        'team_members_profiles': team_members_profiles,
        'home': home
    })