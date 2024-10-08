from django.core.management.base import BaseCommand
from leaderboard.models import Player


class Command(BaseCommand):
    help = 'Resets all players\' mu, sigma, and recalculates rank'

    def handle(self, *args, **kwargs):
        default_mu = 25.0
        default_sigma = 8.33

        players = Player.objects.all()

        for player in players:
            player.mu = default_mu
            player.sigma = default_sigma
            player.rank = default_mu - 3 * default_sigma  # Recalculate the rank
            player.save()

        self.stdout.write(self.style.SUCCESS('Successfully reset mu, sigma, and rank for all players'))
