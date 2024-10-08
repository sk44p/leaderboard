from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404  # Add get_object_or_404 here
from leaderboard.models import Player, Game, Match
from leaderboard.forms import PlayerForm
from openskill.models import PlackettLuce

def leaderboard_view(request):
    players = Player.objects.all().order_by('-rank')  # Order by rank

    # Get the most recent match
    most_recent_match = Match.objects.prefetch_related('games').order_by('-created_at').first()

    player_mu_changes = {}

    # If a match exists, calculate the total mu changes for each player in that match
    if most_recent_match:
        for game in most_recent_match.games.all():
            # Check if red_team_mu_change is not None and matches the number of players
            if game.red_team_mu_change and len(game.red_team_mu_change) == game.red_team.count():
                for i, player in enumerate(game.red_team.all()):
                    if player not in player_mu_changes:
                        player_mu_changes[player] = 0
                    player_mu_changes[player] += game.red_team_mu_change[i]

            # Check if yellow_team_mu_change is not None and matches the number of players
            if game.yellow_team_mu_change and len(game.yellow_team_mu_change) == game.yellow_team.count():
                for i, player in enumerate(game.yellow_team.all()):
                    if player not in player_mu_changes:
                        player_mu_changes[player] = 0
                    player_mu_changes[player] += game.yellow_team_mu_change[i]

    # Prepare the leaderboard data
    leaderboard_data = []
    for player in players:
        mu_change = player_mu_changes.get(player, None)
        leaderboard_data.append({
            'player': player,
            'mu_change': mu_change
        })

    return render(request, 'leaderboard.html', {'players': leaderboard_data})

def create_player_view(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            player = form.save(commit=False)  # Do not save to the database yet
            if not player.avatar:  # Check if avatar is not provided
                player.avatar = None  # Explicitly set to None if no file is uploaded
            player.save()  # Now save the player instance
            return redirect('leaderboard')  # Redirect to the leaderboard or another page
    else:
        form = PlayerForm()
    return render(request, 'create_player.html', {'form': form})


def new_game_view(request):
    if request.method == 'POST':
        red_team_ids = request.POST.get('red_team', '').split(',')
        yellow_team_ids = request.POST.get('yellow_team', '').split(',')

        # Add players to the teams
        red_team_players = Player.objects.filter(id__in=red_team_ids)
        yellow_team_players = Player.objects.filter(id__in=yellow_team_ids)

        # Create a new game
        # Create a new match (or retrieve the match if this is a rematch)
        match_id = request.POST.get('match_id')
        if match_id:
            match = get_object_or_404(Match, id=match_id)
        else:
            match = Match.objects.create()
            match.players.set(red_team_players.union(yellow_team_players))
            match.save()

        # Create a new game and associate it with the match
        new_game = Game.objects.create(match=match)
        new_game.red_team.set(red_team_players)
        new_game.yellow_team.set(yellow_team_players)
        new_game.save()

        # Redirect to the complete_game view for this game
        return redirect('complete_game', game_id=new_game.id)

    else:
        players = Player.objects.all()  # Fetch all players
        return render(request, 'new_game.html', {'players': players})


def complete_game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    red_team = game.red_team.all()
    yellow_team = game.yellow_team.all()

    if request.method == 'POST':
        # Get the winner and losing score from the POST request
        winner = request.POST.get('winner')
        losing_score = request.POST.get('losing_score')

        if losing_score is None or not losing_score.isdigit():
            return render(request, 'complete_game.html', {
                'game': game,
                'red_team': red_team,
                'yellow_team': yellow_team,
                'error': 'Please provide a valid losing score.'
            })

        losing_score = int(losing_score)

        # Set the scores based on the winner
        if winner == 'red':
            game.score_red = 10
            game.score_yellow = losing_score
        else:
            game.score_red = losing_score
            game.score_yellow = 10

        # Mark the game as completed
        game.is_completed = True

        # Example:
        # game.red_team_mu_change = [some logic to calculate mu changes]
        # game.yellow_team_mu_change = [some logic to calculate mu changes]
        model = PlackettLuce()  # Use the PlackettLuce model

        # Create PlackettLuceRating objects for each player
        red_team_ratings = [model.create_rating([player.mu, player.sigma], player.name) for player in red_team]
        yellow_team_ratings = [model.create_rating([player.mu, player.sigma], player.name) for player in yellow_team]
        enum_red = 0
        enum_yellow = 0

        weights = []

        # Determine the ranking based on which team won
        if winner == 'red':
            ranking = [red_team_ratings, yellow_team_ratings]  # Red team wins
            enum_yellow = 1
            weights = [[10.0] * len(red_team), [float(losing_score)]* len(yellow_team)]
        else:
            ranking = [yellow_team_ratings, red_team_ratings]  # Yellow team wins
            enum_red = 1
            weights = [[10.0] * len(yellow_team), [float(losing_score)]* len(red_team)]

        # Use the PlackettLuce model to calculate new ratings
        new_ratings = model.rate(ranking, weights=weights)

        # Track the mu changes for red and yellow team players
        red_team_mu_change = []
        yellow_team_mu_change = []

        # Update the mu and sigma for red team players and calculate the mu change
        for i, player in enumerate(red_team):
            old_mu = player.mu
            new_mu = new_ratings[enum_red][i].mu
            player.mu = new_mu  # Update player's mu
            player.sigma = new_ratings[enum_red][i].sigma  # Update player's sigma
            player.rank = new_ratings[enum_red][i].ordinal()
            player.save()
            red_team_mu_change.append(new_mu - old_mu)  # Calculate and store mu change

        # Update the mu and sigma for yellow team players and calculate the mu change
        for i, player in enumerate(yellow_team):
            old_mu = player.mu
            new_mu = new_ratings[enum_yellow][i].mu
            player.mu = new_mu  # Update player's mu
            player.sigma = new_ratings[enum_yellow][i].sigma  # Update player's sigma
            player.rank = new_ratings[enum_yellow][i].ordinal()
            player.save()
            yellow_team_mu_change.append(new_mu - old_mu)  # Calculate and store mu change

        # Save game scores, mu changes, and mark the game as completed
        game.red_team_mu_change = red_team_mu_change  # Store the mu changes for the red team
        game.yellow_team_mu_change = yellow_team_mu_change  # Store the mu changes for the yellow team
        game.is_completed = True
        # Save the game
        game.save()

        # Check if a rematch was requested
        if 'rematch' in request.POST:
            # Create a new game with swapped teams
            new_game = Game.objects.create(match=game.match)
            new_game.red_team.set(yellow_team)
            new_game.yellow_team.set(red_team)
            new_game.save()

            # Redirect to the new game's complete_game view
            return redirect('complete_game', game_id=new_game.id)

        # If no rematch, redirect to game history
        return redirect('leaderboard')

    return render(request, 'complete_game.html', {
        'game': game,
        'red_team': red_team,
        'yellow_team': yellow_team,
    })

def game_history_view(request):
    matches = Match.objects.prefetch_related('games').order_by('-created_at')  # Get matches in descending order

    match_data = []
    for match in matches:
        games = match.games.all().order_by('played_at')  # Get all games in the match
        match_data.append({
            'match': match,
            'games': [
                {
                    'date': game.played_at,
                    'red_team': game.red_team.all(),
                    'yellow_team': game.yellow_team.all(),
                    'score_red': game.score_red,
                    'score_yellow': game.score_yellow,
                    'red_team_mu_change': game.red_team_mu_change,
                    'yellow_team_mu_change': game.yellow_team_mu_change,
                }
                for game in games
            ]
        })

    return render(request, 'game_history.html', {'matches': match_data})

def set_auth_token(request):
    response = HttpResponse("Token set successfully.")
    response.set_cookie('auth_token', '!dTtjQpGDnWG3P9D4oLH8NAF#WM4fyunG%*Z7^kqc&7bpJwPx&6BuHm#pw!5rAjh8UgAYKzR4zXu%a$$t4$hvd9ZW', max_age=60*60*24*30*24)  # Expires in 30 days
    return response
