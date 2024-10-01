from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from teams.models import UserTeamProfile, Team


# Create your models here.
class Home(models.Model):
  rood_id = models.IntegerField(primary_key=True)
  goal = models.CharField(max_length=500)
  date = models.DateField(default=timezone.now)
  start_date = models.DateField(default=timezone.now)
  end_date = models.DateField(default=timezone.now)
  user_id = models.IntegerField()
  image = models.CharField(max_length=150)
  pos = models.IntegerField()
  is_end = models.BooleanField()
  invitation_num = models.IntegerField()
  user_id2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='homes')

  def __str__(self):
    return self.goal