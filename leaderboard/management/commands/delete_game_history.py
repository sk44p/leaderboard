from django.core.management.base import BaseCommand
from leaderboard.models import Game, Match


class Command(BaseCommand):
    help = 'Deletes all game and match history'

    def handle(self, *args, **kwargs):
        # Delete all Game and Match records
        Game.objects.all().delete()
        Match.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all game and match history.'))
