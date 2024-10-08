from django.core.management.base import BaseCommand
from leaderboard.models import Player, Game

class Command(BaseCommand):
    help = 'Clear test data from the database'

    def handle(self, *args, **kwargs):
        Game.objects.all().delete()
        Player.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Test data cleared successfully'))
