A foosball leaderboard app using the Openskill algorithm to rank players.

SECURITY:
the app has no user authentication, so you need to get the token first, at '/set-token'. 
to "unlock" the site, comment out this line in settings.py: 'leaderboard_app.middleware.TokenAuthMiddleware',
once you've got the token, you can lock the site down again.

USAGE:
after creating players:
select new game
choose the players per side. 
you choose which side won, and then enter the losing side's score.
you can either rematch (which will swap the players' sides) or complete the match.

choosing the side (red or yellow) matters because then we can track if one side of the table provides an advantage or not. we can then make tournaments with "amateurs" fairer if we know that.

choosing the losing score (because the winning score is always 10) just helps with getting to more accurate scores
