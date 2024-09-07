from pickle_match.models.team import Team, Teams
from pickle_match.models.player import Player
from pickle_match.strategy.match_generator import MatchGenerator
from random import shuffle
from collections import Counter, defaultdict
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


    bottom = [ Player(name=player.name, rating=player.rating, score=0) for player in bottom]
    lower = [ Player(name=player.name, rating=player.rating, score=1) for player in lower]
    upper = [ Player(name=player.name, rating=player.rating, score=2) for player in upper]

    # Randomly permute them.
    shuffle(bottom)
    shuffle(lower)
    shuffle(upper)
    

    teams = [ 
        Team(
            players=[bottom[i], lower[i], upper[2*i], upper[2*i+1]], team_id=i+1
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
        # display(HTML(first_matches.to_df(round_no=2*i+1).to_html()))
        mg = MatchGenerator(all_pairs, new_constraints)
        second_matches, _ = mg.generate()
        

        matches.append(second_matches)
    return matches


def _check_each_player_plays_4_or_more_teams(rounds, teams):
    # TODO THIS IS NOT CORRECT
    """
    Each player should play at least 2 other teams. 
    So we keep a map 
    {
      team -> counter<team>
    }
    """
    num_teams = teams.num_teams
    player_to_team = {}
    team_balance_map = defaultdict(Counter)
    for team in teams:
        for player in team.players:
            player_to_team[player] = team.team_id
    
    for tournament_round in rounds:
        for match in tournament_round:
            t1a = match.first.first
            t2a = match.second.first

            first_team = player_to_team[t1a]
            second_team = player_to_team[t2a]

            team_balance_map[first_team][second_team] += 1
            team_balance_map[second_team][first_team] += 1

    # All teams should play all teams
    all_teams_play_all_teams = all([
        len(counter.values()) == (num_teams - 1)
        for counter in team_balance_map.values()
    ])

    # No team should play less than twice
    no_team_only_once = all([
        min(counter.values()) > 1
        for counter in team_balance_map.values()
    ])

    return all_teams_play_all_teams and no_team_only_once


def _check_difficulties(rounds):
    cumulative_difficulties = Counter()

    for tournament_round in rounds:
        difficulties = tournament_round.difficulty_counter
        cumulative_difficulties += difficulties
    
    for difficulty in cumulative_difficulties.values():
        if difficulty < 13 or difficulty > 16:
            return False

    return True


def generate_best_pairings(teams, num_attempts=100000):
    """
    We model pairings as a graph, where each node is 2 players (partners).

    A valid pairing is a graph where every edge has degree 1, with constraints:
        - No partners may play other partners on their team.
        - No partners may player partners that they have played before (in previous rounds).
    """
    
    for i in range(num_attempts):
        if i % 1000 == 0:
            print(f"Simulation {i} did not pass...")
        rounds = generate_pairings(teams)
        if _check_difficulties(rounds):
            if _check_each_player_plays_4_or_more_teams(rounds, teams):
                print(f"Every team played all other teams 2 or more times")
                for i, tournament_round in enumerate(rounds):
                    display(HTML(tournament_round.to_df(round_no=2*i+1).to_html()))
