# Generated by Django 5.1.1 on 2024-10-19 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0011_game_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='red_team_logo',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='yellow_team_logo',
            field=models.URLField(blank=True, null=True),
        ),
    ]
