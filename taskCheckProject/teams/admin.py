from django.contrib import admin
from .models import Team, Invite, UserTeamProfile

admin.site.register(Team)
admin.site.register(Invite)
admin.site.register(UserTeamProfile)
