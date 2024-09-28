from django.core.management.base import BaseCommand
from story.models import Story
from django.utils import timezone

class Command(BaseCommand):
    help = 'Resets stories at midnight by marking them as expired or removing them.'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_stories = Story.objects.filter(expire_time__lt=now)
        expired_stories.update(is_active=False)  # 비활성화하거나 삭제하는 로직
        self.stdout.write(self.style.SUCCESS('Successfully reset expired stories'))
