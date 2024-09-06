from pickle_match.models.team import Team, Teams
from pickle_match.strategy.match_generator import MatchGenerator
from random import shuffle
from IPython.display import display, HTML

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


def generate_pairings(teams):
    average_rating_differences = []
    matches = []
    for i in range(3):
        all_pairs = []
        all_constraints = []
        for team in teams:
            first_pair, second_pair = team.pairs[2*i], team.pairs[2*i + 1]
            all_constraints += team.default_constraints(first_pair) 
            all_constraints += team.default_constraints(second_pair)
            all_pairs.append(first_pair)
            all_pairs.append(second_pair)


        mg = MatchGenerator(all_pairs, all_constraints)
        first_matches, new_constraints = mg.generate()
        matches.append(first_matches)
        average_rating_differences.append(first_matches.average_rating_difference)
        # display(HTML(first_matches.to_df(round_no=2*i+1).to_html()))
        mg = MatchGenerator(all_pairs, new_constraints)
        second_matches, _ = mg.generate()
        
        average_rating_differences.append(second_matches.average_rating_difference)

        matches.append(second_matches)


        # display(HTML(second_matches.to_df(round_no=2*i + 2).to_html()))

    
    total_average_rating_difference = sum(average_rating_differences) / len(average_rating_differences)
    return matches, total_average_rating_difference


def generate_best_pairings(teams, num_attempts=100):
    """
    We model pairings as a graph, where each node is 2 players (partners).

    A valid pairing is a graph where every edge has degree 1, with constraints:
        - No partners may play other partners on their team.
        - No partners may player partners that they have played before (in previous rounds).
    """
    for i in range(num_attempts):
        matches, total_average_rating_difference = generate_pairings(teams)
        print(i, total_average_rating_difference)
