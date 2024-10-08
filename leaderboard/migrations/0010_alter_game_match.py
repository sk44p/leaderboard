# Generated by Django 5.1.1 on 2024-09-25 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0009_match_game_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='leaderboard.match'),
        ),
    ]