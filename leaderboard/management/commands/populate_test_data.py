from django.core.management.base import BaseCommand
from django.utils import timezone
from leaderboard.models import Player, Game, Match
import random

class Command(BaseCommand):
    help = 'Generate test data'

    def handle(self, *args, **kwargs):
        # Create some players
        player_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
        players = []
        for name in player_names:
            player = Player.objects.create(name=name, mu=random.uniform(25, 35), sigma=random.uniform(2, 4))
            players.append(player)

        # Create multiple matches
        for _ in range(5):
            match = Match.objects.create()
            match.players.set(players)

            # Create 2-3 games in each match
            for _ in range(random.randint(2, 3)):
                game = Game.objects.create(match=match)
                game.red_team.set(players[:2])
                game.yellow_team.set(players[2:])
                game.score_red = random.randint(0, 10)
                game.score_yellow = random.randint(0, 10)
                game.red_team_mu_change = [random.uniform(-2, 2) for _ in range(2)]
                game.yellow_team_mu_change = [random.uniform(-2, 2) for _ in range(2)]
                game.played_at = timezone.now()
                game.is_completed = True
                game.save()

        self.stdout.write(self.style.SUCCESS('Test data generated successfully'))
