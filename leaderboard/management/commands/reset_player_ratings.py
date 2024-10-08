from django.core.management.base import BaseCommand
from leaderboard.models import Player


class Command(BaseCommand):
    help = 'Resets all players\' mu and sigma to default values'

    def handle(self, *args, **kwargs):
        default_mu = 25.0
        default_sigma = 8.33

        # Reset all players' mu and sigma values
        Player.objects.all().update(mu=default_mu, sigma=default_sigma)

        # Print a success message
        self.stdout.write(self.style.SUCCESS('Successfully reset mu and sigma for all players'))
