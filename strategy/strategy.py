import sys
from models.team import Team, Teams
from random import shuffle

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def generate_teams(players):
    TEAM_SIZE = 4
    
    assert len(players) % TEAM_SIZE == 0
    num_teams = len(players) // TEAM_SIZE

    # Sort the players by rating
    sorted_players = sorted(players, key=lambda player: player.rating)
    groups = list(chunks(sorted_players, num_teams))

    # Randomly permute them.
    for group in groups: shuffle(group)
    
    # Pick random teams, one from each group.
    teams = [ 
        Team(
            players=[group[i] for group in groups]
        )
        for i in range(num_teams)
    ]
    return Teams(teams=teams)

def generate_best_teams(players, num_attempts=50):
    all_teams = [generate_teams(players) for _ in range(num_attempts)]
    return sorted(all_teams, key=lambda teams: teams.rating_variance)[0]
