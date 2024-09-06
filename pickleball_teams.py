from pickle_match.loaders.load import load_players
from pickle_match.strategy.strategy import generate_best_teams

players = load_players("pickle_match/examples/ratings.csv")
teams = generate_best_teams(players)
print(teams.rating_variance)
# pairings = generate_best_pairings(players)

# TODO:
# - write generate_best_pairings
# - connect to google collab

# Collab should be like:
# - Each team has one player from each quartile ()
# - Average team variance: 2.23xxxx
# 