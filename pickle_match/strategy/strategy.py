from pickle_match.models.team import Team, Teams
from pickle_match.models.player import Player
from pickle_match.models.match import Schedule
from pickle_match.strategy.match_generator import MatchGenerator
from random import shuffle
from collections import Counter, defaultdict

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
    return Schedule(rounds=matches)


def _check_all_teams_play_n_times(schedule, teams, n):
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
    
    for tournament_round in schedule:
        for match in tournament_round:
            t1a = match.first.first
            t2a = match.second.first

            first_team = player_to_team[t1a]
            second_team = player_to_team[t2a]

            team_balance_map[first_team][second_team] += 1
            team_balance_map[second_team][first_team] += 1

    # All teams should play all teams
    if n > 0:
        all_teams_play_all_teams = all([
            len(counter.values()) == (num_teams - 1)
            for counter in team_balance_map.values()
        ])

        # No team should play less than twice
        no_team_only_once = all([
            min(counter.values()) >= n
            for counter in team_balance_map.values()
        ])

        return all_teams_play_all_teams and no_team_only_once
    else:
        return True

def _cum_deviation(schedule, explain=False):
    cumulative_difficulties = schedule.cumulative_difficulties
    cum_deviation = 0

    for difficulty in cumulative_difficulties.values():
        cum_deviation += abs(15-difficulty)
    return cum_deviation

def _check_difficulties(schedule, min_difficulty, max_difficulty, explain=False):
    cumulative_difficulties = schedule.cumulative_difficulties

    for difficulty in cumulative_difficulties.values():
        if difficulty < min_difficulty or difficulty > max_difficulty:
            return False
    return True

def generate_best_pairings(
        teams,
        num_attempts=100000,
        min_difficulty=14,
        max_difficulty=16,
        all_teams_play_at_least=2,
        minimize_deviation=False,
        explain=False,
):
    """
    We model pairings as a graph, where each node is 2 players (partners).

    A valid pairing is a graph where every edge has degree 1, with constraints:
        - No partners may play other partners on their team.
        - No partners may player partners that they have played before (in previous rounds).
    """

    min_deviation = 100000
    best_schedule = None
    
    for i in range(num_attempts):
        if i % 1000 == 0:
            print(f"Simulation {i} did not pass...")
        schedule = generate_pairings(teams)
        if _check_all_teams_play_n_times(schedule, teams, n=all_teams_play_at_least):

            if minimize_deviation:
                deviation = _cum_deviation(schedule)
                if deviation < min_deviation:
                    best_schedule = schedule
                    min_deviation = deviation

            else:
                if _check_difficulties(schedule, min_difficulty, max_difficulty, explain):
                    print(
                        f"""
                        Found a pairing after {i} simulations where:
                            * Everyone has difficulty score {min_difficulty}-{max_difficulty}.
                            * Every team plays every other team {all_teams_play_at_least} times.
                        """
                    )

                    if explain:
                        print(schedule.cumulative_difficulties)
                    schedule.display()
                    return
    
    print(
        f"""
        Found a pairing after {num_attempts} simulations where:
            * Total difficulty deviation was minimized at {min_deviation}
            * Every team plays every other team {all_teams_play_at_least} times.
        """
    )
    if explain:
        print(best_schedule.cumulative_difficulties)
    best_schedule.display()
