from loaders.load import load_players
from strategy.strategy import generate_best_teams

players = load_players("examples/ratings.csv")
teams = generate_best_teams(players)
