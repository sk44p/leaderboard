# Generated by Django 5.1.1 on 2024-09-25 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0007_game_played_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='rank',
            field=models.FloatField(default=0.0),
        ),
    ]