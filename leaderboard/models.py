from django.db import models
from django.utils import timezone

class Player(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    mu = models.FloatField(default=25.0)   # Default starting mu
    sigma = models.FloatField(default=8.33)  # Default starting sigma (standard deviation)
    rank = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    # A helper method to retrieve the player's rating
    def get_rating(self):
        return [self.mu, self.sigma]  # This returns the player's rating in OpenSkill format


class Match(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Time the match was created
    players = models.ManyToManyField(Player)  # Players involved in the match

    def __str__(self):
        return f"Match {self.id} - Created at {self.created_at}"


class Game(models.Model):
    red_team = models.ManyToManyField(Player, related_name='red_team')  # Red team can have 1 or 2 players
    yellow_team = models.ManyToManyField(Player, related_name='yellow_team')  # Yellow team can have 1 or 2 players
    red_team_logo = models.URLField(blank=True, null=True)  # URL for red team logo
    yellow_team_logo = models.URLField(blank=True, null=True)  # URL for yellow team logo
    score_red = models.IntegerField(default=0)
    score_yellow = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    # Add a date field for when the game was played
    played_at = models.DateTimeField(default=timezone.now)

    # Fields to store the mu change for each player after the game
    red_team_mu_change = models.JSONField(null=True, blank=True)  # Store mu changes as JSON
    yellow_team_mu_change = models.JSONField(null=True, blank=True)

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='games')
    winner = models.CharField(max_length=10, choices=[('red', 'Red'), ('yellow', 'Yellow')], blank=True, null=True)

    def __str__(self):
        return f"Game {self.id} - Red Team vs Yellow Team"


