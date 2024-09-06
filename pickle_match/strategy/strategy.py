from pickle_match.models.team import Team, Teams
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

    # Group for bottom 0-25%, 25-50%, 50+%
    bottom, lower, middle, top = list(chunks(sorted_players, num_teams))
    upper = middle + top

    # Randomly permute them.
    shuffle(bottom)
    shuffle(lower)
    shuffle(upper)
    

    teams = [ 
        Team(
            players=[bottom[i], lower[i], upper[2*i], upper[2*i+1]]
        )
        for i in range(num_teams)
    ]
    return Teams(teams=teams)

def generate_best_teams(players, num_attempts=50, explain=False):
    if explain:
        print(f"""

Splitting players into three groups (Bottom Quarter, Lower Quarter, Top Half).

Each team will have 1 player from bottom, 1 from lower, and 2 from top half.

We then create {num_attempts} teams randomly, and choose the one with the lowest rating variance between teams.
              """
        )

    all_teams = [generate_teams(players) for _ in range(num_attempts)]
    return sorted(all_teams, key=lambda teams: teams.rating_variance)[0]


def generate_best_pairings(teams):
    ...
